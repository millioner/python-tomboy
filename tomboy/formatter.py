### -*- coding: utf-8 -*- ###

import re

NOTE_CONVERTING_MAP = (
    ('\n', '<br/>'),

    ('<underline>', '<span style="text-decoration: underline;">'),
    ('<monospace>', '<span style="font-family: monospace;">'),
    ('<italic>', '<span style="font-style: italic;">'),
    ('<highlight>', '<span style="background-color: #faff00;">'),
    ('<strikethrough>', '<span style="text-decoration: line-through;">'),
    ('<bold>', '<b>'),
    ('</bold>', '</b>'),

    ('<list>', '<ul>'),
    ('</list>', '</ul>'),
    ('<list-item', '<li'),
    ('</list-item>', '</li>'),

    ('<size:small>', '<span style="font-size: 12px;">'),
    ('<size:large>', '<span style="font-size: 18px;">'),
    ('<size:huge>', '<span style="font-size: 26px;">'),

    (('<link:url>', '</link:url>'), ''),

    ([
         '</underline>',
         '</monospace>',
         '</italic>',
         '</highlight>',
         '</strikethrough>',
         '</size:small>',
         '</size:large>',
         '</size:huge>'
     ], '</span>')
)

def convert_note_to_html(note_content):
    for rule in NOTE_CONVERTING_MAP:
        placeholders = rule[0] if type(rule[0]) in (list, tuple) else (rule[0], )
        for placeholder in placeholders:
            note_content = note_content.replace(placeholder, rule[1])

    # TODO: links
    return '<pre style="font-family: serif;">%s</pre>' % note_content