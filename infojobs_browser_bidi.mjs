/**
 * InfoJobs: lectura única de candidaturas desde Firefox/WebDriver BiDi.
 * Solo localhost; sin cookies exportadas, contraseñas ni API privada.
 * --login recibe por STDIN credenciales del programa local (solo si caduca la sesión).
 * No mostrar, persistir ni registrar secretos.
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';

export const TRUSTED_HOST = 'www.infojobs.net';
export const APPLICATIONS_URL = 'https://www.infojobs.net/candidate/applications/list.xhtml';
const SOCKET_URL = 'ws://127.0.0.1:9222/session';
const PRIVATE_DIR = path.join(os.homedir(), '.local/share/buscar-curro');
const PRIVATE_REPORT = path.join(PRIVATE_DIR,'infojobs_privado.json');
const MAX_FIELD = 320;

export function allowedUrl(u) {
  try {const v=new URL(u); return v.protocol==='https:'&&v.hostname===TRUSTED_HOST&&!v.username&&!v.password&&(!v.port||v.port==='443');}
  catch {return false;}
}
export function primitive(node) {
  if (!node || typeof node!=='object') return undefined;
  if (node.type==='object') return Object.fromEntries((node.value||[]).map(([k,v])=>[k,primitive(v)]));
  if (node.type==='array') return (node.value||[]).map(primitive);
  if (['string','number','boolean','null','undefined'].includes(node.type))return node.value;
  return undefined;
}
export function sanitizeItem(row) {
  if (!row || typeof row.title!=='string'||!row.title.trim())return null;
  const clean=x=>String(x||'').replace(/[\r\n\t]+/g,' ').replace(/\s+/g,' ').trim().slice(0,MAX_FIELD);
  return {
    title:clean(row.title),
    company:clean(row.company),
    status:clean(row.status),
    recent_activity:clean(row.recent_activity)
  };
}
export function privateReport(data, when=new Date().toISOString()) {
  if (!data || data.trusted!==true || data.private!==true || !Array.isArray(data.items) || (data.items.length===0 && data.emptyKnown!==true))
    throw Error('private_read_unverified');
  if (data.items.length>100) throw Error('suspiciously_many_items');
  const items=data.items.map(sanitizeItem).filter(Boolean);
  return {schema_version:1,checked_at:when,portal:'InfoJobs',
          status:'private_read_verified',applications_count:items.length,
          applications:items,warning:'Estado observado en la sesion del navegador; no implica entrevista'};
}
export function savePrivate(report,dir=PRIVATE_DIR) {
  const s=fs.lstatSync(dir);
  if(!s.isDirectory()||s.isSymbolicLink()||(s.mode&0o077)!==0||s.uid!==process.getuid())
    throw Error('private_folder_permissions_invalid');
  const file=path.join(dir,'infojobs_privado.json');
  if(fs.existsSync(file)&&fs.lstatSync(file).isSymbolicLink()) throw Error('report_symlink_denied');
  const tmp=path.join(dir,'.infojobs-'+crypto.randomUUID()+'.tmp');
  try {
    fs.writeFileSync(tmp,JSON.stringify(report,null,2)+'\n',{mode:0o600,flag:'wx'});
    fs.renameSync(tmp,file);
    fs.chmodSync(file,0o600);
  } finally { if(fs.existsSync(tmp))fs.unlinkSync(tmp); }
}
class Browser {
  constructor() {
    this.ws=new WebSocket(SOCKET_URL);
    this.next=0;this.pending=new Map();this.hasSession=false;
    this.ws.addEventListener('message',e=>{
      let m;
      try {m=JSON.parse(e.data)}catch{return}
      if(typeof m.id!=='number')return;
      const p=this.pending.get(m.id);if(!p)return;
      this.pending.delete(m.id);clearTimeout(p.timer);
      if(m.error)p.reject(Error('bidi_'+String(m.error).slice(0,100)));
      else p.resolve(m.result);
    });
  }
  async open() {
    await new Promise((resolve,reject)=>{
      const timer=setTimeout(()=>reject(Error('browser_connection_timeout')),6500);
      this.ws.addEventListener('open',()=>{clearTimeout(timer);resolve()},{once:true});
      this.ws.addEventListener('error',()=>{clearTimeout(timer);reject(Error('browser_connection_failed'))},{once:true});
    });
    await this.call('session.new',{capabilities:{alwaysMatch:{}}});this.hasSession=true;
  }
  async call(method,params={}) {
    return new Promise((resolve,reject)=>{
      const id=++this.next;
      const timer=setTimeout(()=>{this.pending.delete(id);reject(Error('bidi_timeout'))},12000);
      this.pending.set(id,{resolve,reject,timer});
      this.ws.send(JSON.stringify({id,method,params}));
    });
  }
  async context() {
    const root=await this.call('browsingContext.getTree',{});
    const entry=root.contexts?.find(c=>allowedUrl(c.url));
    if (entry)return entry.context;
    // Firefox can expose about:blank before restoring its InfoJobs tab.
    // Create a fresh tab instead of navigating an unrelated user tab.
    if (!Array.isArray(root.contexts)||root.contexts.length>10)
      throw Error('no_infojobs_browser_tab');
    const created=await this.call('browsingContext.create',{type:'tab'});
    if(!created?.context)throw Error('no_infojobs_browser_tab');
    return created.context;
  }
  async evaluate(context,expression) {
    const r=await this.call('script.evaluate',{expression,target:{context},awaitPromise:false,resultOwnership:'none'});
    if(r.type!=='success')throw Error('script_evaluation_failed');
    return primitive(r.result);
  }
  async close(){if(this.hasSession){try{await this.call('session.end',{});}catch{}}this.ws.close();}
}
const DOM_READ=`(()=>{
  if(location.protocol!=='https:'||location.hostname!=='www.infojobs.net')
    return {trusted:false};
  const text=document.body?.innerText||'';
  const isPrivate=location.pathname.includes('/candidate/applications/list.xhtml')
   &&text.includes('Mis ofertas')&&text.includes('CANDIDATURAS');
  const requiresLogin=!!document.querySelector('input[type="password"]')
   &&!!document.querySelector('input[type="email"]');
  const links=[...document.querySelectorAll('a[href*="/candidate/applications/list-events.xhtml"]')];
  const items=links.slice(0,100).map(a=>{
    const block=a.parentElement?.parentElement;
    const lines=(block?.innerText||'').split(/\\n+/).map(t=>t.trim()).filter(Boolean);
    const title=(a.innerText||a.textContent||'').trim();
    const pos=lines.findIndex(t=>t.includes(title));
    const company=pos>=0?lines[pos+1]||'':'';
    const status=lines.find(t=>/^(Inscrito|En proceso|Descartado|Finalista|Entrevista|Seleccionado)$/i.test(t))||'';
    const recent_activity=lines.find(t=>/^Hace\\s+\\d+/i.test(t))||'';
    return {title,company,status,recent_activity};
  });
  const emptyKnown=/no tienes candidaturas|ninguna candidatura/i.test(text);
  return {trusted:true,private:isPrivate,requiresLogin,emptyKnown,
          pathname:location.pathname,items};
})()`;
const DOM_AUTH=`(username,password)=>{
  if(location.protocol!=='https:'||location.hostname!=='www.infojobs.net'
     ||!location.pathname.includes('candidate-login'))
    return 'untrusted_or_not_login';
  const email=document.querySelector('input[name="email"][type="email"]');
  const pass=document.querySelector('input[name="password"][type="password"]');
  const submit=email?.closest('form')?.querySelector('button[type="submit"]')
    ||document.querySelector('button[type="submit"]');
  if(!email||!pass||!submit) return 'login_form_unrecognized';
  for(const [el,val] of [[email,username],[pass,password]]){
    const setter=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;
    setter.call(el,val);
    el.dispatchEvent(new Event('input',{bubbles:true}));
    el.dispatchEvent(new Event('change',{bubbles:true}));
  }
  submit.click();
  return 'submitted_once';
}`;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function read(browser){
 const context=await browser.context();
 await browser.call('browsingContext.navigate',{context,url:APPLICATIONS_URL,wait:'none'});
 for(let i=0;i<9;i++){
   await sleep(650);
   const r=await browser.evaluate(context,DOM_READ);
   if(!r?.trusted)throw Error('site_origin_unverified');
   if(r.private && (r.items?.length>0 || r.emptyKnown))
     return {status:'private_read_verified',report:privateReport(r)};
   if(r.requiresLogin)return {status:'authentication_required'};
 }
 return {status:'private_read_unverified'};
}
async function login(browser) {
 const context=await browser.context();
 const preflight=await browser.evaluate(context,"({host:location.hostname,proto:location.protocol,path:location.pathname})");
 if(preflight?.host!=='www.infojobs.net'||preflight?.proto!=='https:'
    ||!String(preflight.path).includes('candidate-login'))return {status:'login_form_unrecognized'};
 let credentials=null;
 try {
   const chunks=[];
   for await(const c of process.stdin) {chunks.push(c);if(chunks.reduce((a,b)=>a+b.length,0)>18000)throw Error('too_much_input')}
   credentials=JSON.parse(Buffer.concat(chunks).toString('utf8'));
   if(typeof credentials.username!=='string'||typeof credentials.password!=='string'
      ||!credentials.username||!credentials.password)throw Error('invalid_input');
   const result=await browser.call('script.callFunction',{
     functionDeclaration:DOM_AUTH,
     arguments:[{type:'string',value:credentials.username},{type:'string',value:credentials.password}],
     target:{context},awaitPromise:false,resultOwnership:'none'
   });
   const status=primitive(result.result);
   if(status!=='submitted_once')return {status:'login_form_unrecognized'};
   await sleep(3500);
   const current=await browser.evaluate(context,DOM_READ);
   return {status:current?.requiresLogin?'interaction_or_login_required':'login_submitted_check_session'};
 }finally {credentials=null;}
}
async function main() {
 const mode=process.argv[2];
 if(!['--revisar','--iniciar-sesion'].includes(mode))throw Error('argument_invalid');
 const browser=new Browser();
 try {
  await browser.open();
  const r=mode==='--revisar'?await read(browser):await login(browser);
  if(r.report)savePrivate(r.report);
  const summary={status:r.status,applications:r.report?.applications_count??null};
  console.log(JSON.stringify(summary));
  process.exitCode=r.status==='private_read_verified'||r.status==='login_submitted_check_session'?0:2;
 }finally{await browser.close();}
}
if (process.argv[1] && import.meta.url===new URL('file://'+process.argv[1]).href) {
  main().catch(e=>{
    const safe=['bidi_session_not_created','no_infojobs_browser_tab','site_origin_unverified',
      'script_evaluation_failed','bidi_timeout','browser_connection_timeout',
      'private_folder_permissions_invalid','private_read_unverified'];
    console.log(JSON.stringify({status:'browser_unavailable_or_unverified',
      reason:safe.includes(e.message)?e.message:(e.message.startsWith('bidi_session not created')?'bidi_session_not_created':'other')}));
    process.exitCode=2;
  });
}
