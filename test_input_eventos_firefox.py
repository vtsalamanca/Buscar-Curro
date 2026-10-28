"""Safe unit tests: no live secrets, network, or external accounts."""
import unittest
from input_eventos_firefox import UnsafeTarget, focus_and_fill, valid_screen_point


class FakeText:
    def __init__(self):
        self.text = ""
    def get_character_count(self):
        return len(self.text)


class Field:
    def __init__(self, role="password text"):
        self.role=role
        self.text=FakeText()
    def get_role_name(self):
        return self.role
    def get_text_iface(self):
        return self.text


class Keyboard:
    def __init__(self,field,wrong_focus=False):
        self.field=field
        self.events=[]
        self.wrong_focus=wrong_focus
    def prepare(self,value):
        self.events.append("preflight")
        if any(not 32<=ord(c)<=126 for c in value):
            raise UnsafeTarget("unsupported_character")
    def click(self,window_id,x,y):
        self.events.append("click")
    def type_ascii(self,value):
        self.events.append("typed")
        if not self.wrong_focus:
            self.field.text.text += value
    def clear_with_control_a(self):
        self.events.append("clear")
        self.field.text.text=""


class NativeInputEventsTest(unittest.TestCase):
    def test_safe_sentinel_precedes_synthetic_value(self):
        field=Field()
        keyboard=Keyboard(field)
        focus_and_fill(field,"SYNTHETIC-@123!",keyboard,1,170,374)
        self.assertEqual(field.text.text,"SYNTHETIC-@123!")
        self.assertEqual(keyboard.events,
                         ["preflight","click","typed","clear","typed"])

    def test_no_real_value_typed_if_target_not_proven(self):
        field=Field()
        keyboard=Keyboard(field,wrong_focus=True)
        with self.assertRaisesRegex(UnsafeTarget,"native_focus_not_proven"):
            focus_and_fill(field,"SYNTHETIC",keyboard,1,170,374)
        self.assertEqual(field.text.text,"")
        self.assertEqual(keyboard.events,["preflight","click","typed"])

    def test_non_ascii_fails_before_click(self):
        field=Field()
        keyboard=Keyboard(field)
        with self.assertRaisesRegex(UnsafeTarget,"unsupported_character"):
            focus_and_fill(field,"ficticia-ñ",keyboard,1,170,374)
        self.assertEqual(keyboard.events,["preflight"])

    def test_wrong_role_fails_before_action(self):
        field=Field("button")
        keyboard=Keyboard(field)
        with self.assertRaisesRegex(UnsafeTarget,"field_role_invalid"):
            focus_and_fill(field,"SYNTHETIC",keyboard,1,170,374)
        self.assertEqual(keyboard.events,[])

    def test_bad_values_rejected(self):
        for v in ["",None,5,"a"*8193]:
            field=Field()
            keyboard=Keyboard(field)
            with self.assertRaisesRegex(UnsafeTarget,"value_invalid"):
                focus_and_fill(field,v,keyboard,1,170,374)
            self.assertEqual(keyboard.events,[])

    def test_screen_geometry_conservative(self):
        self.assertTrue(valid_screen_point(150,353,388,48))
        for item in [(-1,-1,-1,-1),(0,0,0,20),(0,0,20,0),(5995,3995,20,20),(1.0,0,20,20)]:
            self.assertFalse(valid_screen_point(*item))


if __name__=="__main__":
    unittest.main()
