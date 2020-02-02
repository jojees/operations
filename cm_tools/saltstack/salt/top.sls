# $Id: d1d18fe3c3a48569735345d6778c07b465de95e1 $

{%- set allstates = salt['cp.list_states']() %}

base:
    '*':
        - users
        - recipes
