import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {allowedUrl,primitive,privateReport,savePrivate,unverifiedDiagnostics} from './infojobs_browser_bidi.mjs';
test('allowlist HTTPS official host only',()=>{
 assert.equal(allowedUrl('https://www.infojobs.net/candidate/applications/list.xhtml'),true);
 for(const u of ['http://www.infojobs.net/','https://infojobs.net/','https://www.infojobs.net.evil.com/','https://bad:bad@www.infojobs.net/','javascript:1'])assert.equal(allowedUrl(u),false);
});
test('remote serializer maps to JSON',()=>{
 assert.deepEqual(primitive({type:'object',value:[['trusted',{type:'boolean',value:true}],['items',{type:'array',value:[]}]]}),{trusted:true,items:[]});
});
test('reject unverified login data',()=>{
 assert.throws(()=>privateReport({trusted:true,private:false,items:[]}),/unverified/);
});
test('persist minimized private results',()=>{
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'bc-bidi-test-'));fs.chmodSync(dir,0o700);
 try {
 const r=privateReport({trusted:true,private:true,items:[{title:'Psicología',company:'Empresa',status:'Inscrito',recent_activity:'Hace 1h',password:'SECRET'}]},'2026-10-27T00:00:00Z');
 savePrivate(r,dir);
 const file=path.join(dir,'infojobs_privado.json');
 assert.equal(fs.statSync(file).mode&0o777,0o600);
 assert.equal(r.applications_count,1);
 assert.equal(fs.readFileSync(file,'utf8').includes('SECRET'),false);
 }finally{fs.rmSync(dir,{recursive:true,force:true})}
});
test('refuse symlinked private directory',()=>{
 const temp=fs.mkdtempSync(path.join(os.tmpdir(),'bc-bidi-test-'));
 const target=path.join(temp,'p');fs.mkdirSync(target,{mode:0o700});
 const alias=path.join(temp,'alias');fs.symlinkSync(target,alias);
 try{assert.throws(()=>savePrivate(privateReport({trusted:true,private:true,items:[],emptyKnown:true}),alias),/permissions/);}
 finally{fs.rmSync(temp,{recursive:true,force:true})}
});

test('reject empty async loading state without explicit empty marker',()=>{
 assert.throws(()=>privateReport({trusted:true,private:true,items:[]}),/unverified/);
 assert.equal(privateReport({trusted:true,private:true,items:[],emptyKnown:true}).applications_count,0);
});

test('unverified diagnosis exposes no page contents or secrets',()=>{
 const d=unverifiedDiagnostics({route_kind:'login',application_links:3,has_login_password:true,
     has_application_headings:false,password:'TOPSECRET',user:'PII'});
 assert.deepEqual(d,{route_kind:'login',application_links:3,has_login_password:true,has_application_headings:false});
 assert.equal(JSON.stringify(d).includes('TOPSECRET'),false);
 assert.deepEqual(unverifiedDiagnostics({route_kind:'https://malicious.invalid',application_links:1000}),
 {route_kind:'unknown',application_links:100,has_login_password:false,has_application_headings:false});
});
