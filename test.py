import unittest
from unittest.mock import patch, MagicMock

import streamlit as st
from streamlit_chat import message
from chat import chatgpt_mini, get_text


class TestApp(unittest.TestCase):

    @patch('openai.Completion.create')
    def test_chatgpt_mini(self, mock_create):
        input_text = "Hi, how are you?"
        history_input = []

        mock_create.return_value.choices[0].text = "I'm fine, thank you. How can I assist you?"

        output = chatgpt_mini(input_text, history_input)

        self.assertEqual(len(output), 2)
        self.assertEqual(output[0], [(input_text, mock_create.return_value.choices[0].text)])
        self.assertEqual(output[1], [(input_text, mock_create.return_value.choices[0].text)])

    def test_get_text(self):
        with patch.object(st, 'text_input', return_value='Hi, how are you?'):
            self.assertEqual(get_text(), 'Hi, how are you?')

if __name__ == '__main__':
    unittest.main()
