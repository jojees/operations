{# Get list of all salt states #}
{%- set allstates = salt['cp.list_states']() %}
{%- set install_apps = [] -%}

{# Iterate through the customstates grain and create array of #}
{# states that we actually have salt states for #}
{%- for app in grains.get('recipes', []) -%}
    {%- if "recipes.%s" % app in allstates -%}
        {%- do install_apps.append("recipes.%s" % app)  -%}
    {%- elif app in allstates -%}
        {%- do install_apps.append(app)  -%}
    {%- endif -%}
{%- endfor -%}

{% if install_apps|count > 0 %}
include:
    {% for app in install_apps %}
    - {{ app }}
    {% endfor %}
{% endif %}
