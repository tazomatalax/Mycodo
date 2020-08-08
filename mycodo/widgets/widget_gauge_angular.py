# coding=utf-8
#
#  widget_gauge_angular.py - Angular Gauge dashboard widget
#
#  Copyright (C) 2017  Kyle T. Gabriel
#
#  This file is part of Mycodo
#
#  Mycodo is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Mycodo is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Mycodo. If not, see <http://www.gnu.org/licenses/>.
#
#  Contact at kylegabriel.com
#
import json
import logging
import re

from flask import flash
from flask_babel import lazy_gettext

logger = logging.getLogger(__name__)


def is_rgb_color(color_hex):
    """
    Check if string is a hex color value for the web UI
    :param color_hex: string to check if it represents a hex color value
    :return: bool
    """
    return bool(re.compile(r'#[a-fA-F0-9]{6}$').match(color_hex))


def custom_colors_gauge_str(form, error):
    sorted_colors_string = ''
    colors_hex = {}
    # Combine all color form inputs to dictionary
    for key in form.keys():
        if ('color_hex_number' in key or
                'color_low_number' in key or
                'color_high_number' in key):
            if int(key[17:]) not in colors_hex:
                colors_hex[int(key[17:])] = {}
        if 'color_hex_number' in key:
            for value in form.getlist(key):
                if not is_rgb_color(value):
                    error.append('Invalid hex color value')
                colors_hex[int(key[17:])]['hex'] = value
        elif 'color_low_number' in key:
            for value in form.getlist(key):
                colors_hex[int(key[17:])]['low'] = value
        elif 'color_high_number' in key:
            for value in form.getlist(key):
                colors_hex[int(key[17:])]['high'] = value

    # Build string of colors and associated gauge values
    for i, _ in enumerate(colors_hex):
        try:
            sorted_colors_string += "{},{},{}".format(
                colors_hex[i]['low'],
                colors_hex[i]['high'],
                colors_hex[i]['hex'])
            if i < len(colors_hex) - 1:
                sorted_colors_string += ";"
        except Exception as err_msg:
            error.append(err_msg)
    return sorted_colors_string, error


def gauge_reformat_stops(current_stops, new_stops, current_colors=None):
    """Generate stops and colors for new and modified gauges"""
    if current_colors:
        colors = current_colors
    else:  # Default colors (adding new gauge)
        colors = '0,20,#33CCFF;20,40,#55BF3B;40,60,#DDDF0D;60,80,#DF5353'

    if new_stops > current_stops:
        stop = 80
        for _ in range(new_stops - current_stops):
            stop += 20
            colors += ';{low},{high},#DF5353'.format(low=stop - 20, high=stop)
    elif new_stops < current_stops:
        colors_list = colors.split(';')
        colors = ';'.join(colors_list[: len(colors_list) - (current_stops - new_stops)])
    new_colors = colors

    return new_colors


def execute_at_creation(new_widget, dict_widget):
    color_list = ["#33CCFF", "#55BF3B", "#DDDF0D", "#DF5353"]
    custom_options_json = json.loads(new_widget.custom_options)

    if custom_options_json['stops'] < 2:
        custom_options_json['stops'] = 2

    stop = custom_options_json['min']
    max = custom_options_json['max']
    difference = int(max - stop)
    stop_size = int(difference / custom_options_json['stops'])
    colors = '{low},{high},{color}'.format(low=stop, high=stop + stop_size, color=color_list[0])
    for i in range(custom_options_json['stops'] - 1):
        stop += stop_size
        if i < len(color_list):
            color = color_list[i + 1]
        else:
            color = "#DF5353"
        colors += ';{low},{high},{color}'.format(low=stop, high=stop + stop_size, color=color)

    custom_options_json['range_colors'] = colors
    new_widget.custom_options = json.dumps(custom_options_json)
    return new_widget


def execute_at_modification(
        mod_widget,
        request_form,
        custom_options_json_presave,
        custom_options_json_postsave):
    allow_saving = True
    error = []

    sorted_colors_string, error = custom_colors_gauge_str(request_form, error)
    sorted_colors_string = gauge_reformat_stops(
        custom_options_json_presave['stops'],
        custom_options_json_postsave['stops'],
        current_colors=sorted_colors_string)

    custom_options_json_postsave['range_colors'] = sorted_colors_string
    return allow_saving, mod_widget, custom_options_json_postsave


def generate_page_variables(widget_unique_id, widget_options):
    # Retrieve custom colors for gauges
    colors_gauge_angular = []
    try:
        if 'range_colors' in widget_options and widget_options['range_colors']:  # Split into list
            color_areas = widget_options['range_colors'].split(';')  # Split into list
        else:  # Create empty list
            color_areas = []
        for each_range in color_areas:
            colors_gauge_angular.append({
                'low': each_range.split(',')[0],
                'high': each_range.split(',')[1],
                'hex': each_range.split(',')[2]})
    except IndexError:
        flash("Colors Index Error", "error")

    return {"colors_gauge_angular": colors_gauge_angular}


def constraints_pass_positive_value(mod_widget, value):
    """
    Check if the user widget is acceptable
    :param mod_widget: SQL object with user-saved Input options
    :param value: float or int
    :return: tuple: (bool, list of strings)
    """
    errors = []
    all_passed = True
    # Ensure value is positive
    if value <= 0:
        all_passed = False
        errors.append("Must be a positive value")
    return all_passed, errors, mod_widget


WIDGET_INFORMATION = {
    'widget_name_unique': 'WIDGET_GAUGE_ANGULAR',
    'widget_name': 'Gauge (Angular)',
    'widget_library': '',
    'no_class': True,

    'message': 'This widget will display a angular gauge.',

    'execute_at_creation': execute_at_creation,
    'execute_at_modification': execute_at_modification,
    'generate_page_variables': generate_page_variables,

    'widget_width': 4,
    'widget_height': 5,

    'custom_options': [
        {
            'id': 'measurement',
            'type': 'select_measurement',
            'default_value': '',
            'options_select': [
                'Input',
                'Math',
                'PID'
            ],
            'name': lazy_gettext('Measurement'),
            'phrase': lazy_gettext('Select a measurement to display')
        },
        {
            'id': 'max_measure_age',
            'type': 'integer',
            'default_value': 120,
            'required': True,
            'constraints_pass': constraints_pass_positive_value,
            'name': lazy_gettext('Measurement Max Age'),
            'phrase': lazy_gettext('The maximum age (seconds) of the measurement')
        },
        {
            'id': 'refresh_seconds',
            'type': 'float',
            'default_value': 30.0,
            'constraints_pass': constraints_pass_positive_value,
            'name': 'Widget Refresh (seconds)',
            'phrase': 'The period of time between refreshing the widget'
        },
        {
            'id': 'min',
            'type': 'float',
            'default_value': 0,
            'name': 'Minimum',
            'phrase': 'The gauge minimum'
        },
        {
            'id': 'max',
            'type': 'float',
            'default_value': 100,
            'name': 'Maximum',
            'phrase': 'The gauge maximum'
        },
        {
            'id': 'stops',
            'type': 'integer',
            'default_value': 4,
            'name': 'Stops',
            'phrase': 'The number of color stops'
        }
    ],

    'widget_dashboard_head': """<script type="text/javascript" src="/static/js/modules/solid-gauge.js"></script>""",

    'widget_dashboard_title_bar': """<span style="padding-right: 0.5em; font-size: {{each_widget.font_em_name}}em">{{each_widget.name}}</span>""",

    'widget_dashboard_body': """<div class="not-draggable" id="container-gauge-{{each_widget.unique_id}}" style="position: absolute; left: 0; top: 0; bottom: 0; right: 0; overflow: hidden;"></div>""",

    'widget_dashboard_configure_options': """
            {% for n in range(widget_variables['colors_gauge_angular']|length) %}
              {% set index = '{0:0>2}'.format(n) %}
        <div class="form-row">
          <div class="col-auto">
            <label class="control-label" for="color_low_number{{index}}">[{{n}}] Low</label>
            <div>
              <input class="form-control" id="color_low_number{{index}}" name="color_low_number{{index}}" type="text" value="{{widget_variables['colors_gauge_angular'][n]['low']}}">
            </div>
          </div>
          <div class="col-auto">
            <label class="control-label" for="color_high_number{{index}}">[{{n}}] High</label>
            <div>
              <input class="form-control" id="color_high_number{{index}}" name="color_high_number{{index}}" type="text" value="{{widget_variables['colors_gauge_angular'][n]['high']}}">
            </div>
          </div>
          <div class="col-auto">
            <label class="control-label" for="color_hex_number{{index}}">[{{n}}] Color</label>
            <div>
              <input id="color_hex_number{{index}}" name="color_hex_number{{index}}" placeholder="#000000" type="color" value="{{widget_variables['colors_gauge_angular'][n]['hex']}}">
            </div>
          </div>
        </div>
            {% endfor %}
""",

    'widget_dashboard_js': """<!-- No JS content -->""",

    'widget_dashboard_js_ready': """
  function getLastDataGaugeAngular(chart_number,
                       unique_id,
                       measure_type,
                       measurement_id,
                       max_measure_age_sec) {
    if (decimal_places === null) {
      decimal_places = 1;
    }

    const url = '/last/' + unique_id + '/' + measure_type + '/' + measurement_id + '/' + max_measure_age_sec.toString();
    $.ajax(url, {
      success: function(data, responseText, jqXHR) {
        if (jqXHR.status === 204) {
          chart[chart_number].series[0].points[0].update(null);
        }
        else {
          const formattedTime = epoch_to_timestamp(data[0]);
          const measurement = data[1];
          chart[chart_number].series[0].points[0].update(measurement);
          //document.getElementById('timestamp-' + chart_number).innerHTML = formattedTime;
        }
      },
      error: function(jqXHR, textStatus, errorThrown) {
        chart[chart_number].series[0].points[0].update(null);
      }
    });
  }

  // Repeat function for getLastDataGaugeAngular()
  function repeatLastDataGaugeAngular(chart_number,
                          dev_id,
                          measure_type,
                          measurement_id,
                          period_sec,
                          max_measure_age_sec) {
    setInterval(function () {
      getLastDataGaugeAngular(chart_number,
                  dev_id,
                  measure_type,
                  measurement_id,
                  max_measure_age_sec)
    }, period_sec * 1000);
  }
""",

    'widget_dashboard_js_ready_end': """
{%- set device_id = widget_options['measurement'].split(",")[0] -%}
{%- set measurement_id = widget_options['measurement'].split(",")[1] -%}

{% set measure = { 'measurement_id': None } %}
  chart[{{chart_number}}] = new Highcharts.chart({
    chart: {
      renderTo: 'container-gauge-{{each_widget.unique_id}}',
      type: 'gauge',
      plotBackgroundColor: null,
      plotBackgroundImage: null,
      plotBorderWidth: 0,
      plotShadow: false,
      events: {
        load: function () {
          {% for each_input in input  if each_input.unique_id == device_id %}
          getLastDataGaugeAngular({{chart_number}}, '{{device_id}}', 'input', '{{measurement_id}}', {{widget_options['max_measure_age']}});
          repeatLastDataGaugeAngular({{chart_number}}, '{{device_id}}', 'input', '{{measurement_id}}', {{widget_options['refresh_seconds']}}, {{widget_options['max_measure_age']}});
          {%- endfor -%}

          {% for each_math in math if each_math.unique_id == device_id %}
          getLastDataGaugeAngular({{chart_number}}, '{{device_id}}', 'math', '{{measurement_id}}', {{widget_options['max_measure_age']}});
          repeatLastDataGaugeAngular({{chart_number}}, '{{device_id}}', 'math', '{{measurement_id}}', {{widget_options['refresh_seconds']}}, {{widget_options['max_measure_age']}});
          {%- endfor -%}

          {%- for each_pid in pid if each_pid.unique_id == device_id %}
          getLastDataGaugeAngular({{chart_number}}, '{{device_id}}', 'pid', '{{measurement_id}}', {{widget_options['max_measure_age']}});
          repeatLastDataGaugeAngular({{chart_number}}, '{{device_id}}', 'pid', '{{measurement_id}}', {{widget_options['refresh_seconds']}}, {{widget_options['max_measure_age']}});
          {%- endfor -%}
        }
      },
      spacingTop: 0,
      spacingLeft: 0,
      spacingRight: 0,
      spacingBottom: 0
    },

    title: null,

    exporting: {
      enabled: false
    },

    pane: {
        startAngle: -150,
        endAngle: 150,
        background: [{
            backgroundColor: '#c1c1c1',
            borderWidth: 0,
            outerRadius: '105%',
            innerRadius: '103%'
        }]
    },

    // the value axis
    yAxis: {
        min: {{widget_options['min']}},
        max: {{widget_options['max']}},
        title: {
      {%- if measurement_id in dict_measure_units and
             dict_measure_units[measurement_id] in dict_units and
             dict_units[dict_measure_units[measurement_id]]['unit'] -%}
          text: '{{dict_units[dict_measure_units[measurement_id]]['unit']}}',
      {% else %}
          text: '',
      {%- endif -%}
          y: 20
        },

        minColor: "#3e3f46",
        maxColor: "#3e3f46",

        minorTickInterval: 'auto',
        minorTickWidth: 1,
        minorTickLength: 10,
        minorTickPosition: 'inside',
        minorTickColor: '#666',

        tickPixelInterval: 30,
        tickWidth: 2,
        tickPosition: 'inside',
        tickLength: 10,
        tickColor: '#666',
        labels: {
            step: 2,
            rotation: 'auto'
        },
        plotBands: [
          {% for n in range(widget_variables['colors_gauge_angular']|length) %}
            {% set index = '{0:0>2}'.format(n) %}
        {
            from: {{widget_variables['colors_gauge_angular'][n]['low']}},
            to: {{widget_variables['colors_gauge_angular'][n]['high']}},
            color: '{{widget_variables['colors_gauge_angular'][n]['hex']}}'
        },
          {% endfor %}
        ]
    },

    series: [{
        name: '
        {%- for each_input in input if each_input.unique_id == device_id -%}
          {%- if measurement_id in device_measurements_dict -%}
          {{each_input.name}} (
            {%- if not device_measurements_dict[measurement_id].single_channel -%}
              {{'CH' + (device_measurements_dict[measurement_id].channel|int)|string + ', '}}
            {%- endif -%}
          {{dict_measurements[device_measurements_dict[measurement_id].measurement]['name']}}
          {%- endif -%}
        {%- endfor -%}

        {%- for each_math in math if each_math.unique_id == device_id -%}
          {{each_math.measure|safe}}
        {%- endfor -%}

        {%- for each_pid in pid if each_pid.unique_id == device_id -%}
          {{each_pid.measure|safe}}
        {%- endfor -%})',
        data: [null],
        dataLabels: {
          style: {"fontSize": "14px"},
          format: '{point.y:,.1f}'
        },
        yAxis: 0,
          dial: {
            backgroundColor: '{% if current_user.theme in dark_themes %}#e3e4f4{% else %}#3e3f46{% endif %}',
            baseWidth: 5
        },
        tooltip: {

        {%- for each_input in input if each_input.unique_id == device_id %}
             pointFormatter: function () {
              return '<span style="color:'+ this.series.color + '"">\u25CF</span> ' + this.series.name + ':<b> ' + Highcharts.numberFormat(this.y, 2) + ' {{dict_units[device_measurements_dict[measurement_id].unit]['unit']}}</b><br>';
            },
        {%- endfor -%}

            valueSuffix: '
        {%- for each_input in input if each_input.unique_id == device_id -%}
          {{' ' + dict_units[device_measurements_dict[measurement_id].unit]['unit']}}
        {%- endfor -%}

        {%- for each_math in math if each_math.unique_id == device_id -%}
          {{' ' + each_math.measure_units|safe}}
        {%- endfor -%}

        {%- for each_pid in pid if each_pid.unique_id == device_id -%}
          {{' ' + each_pid.measure_units|safe}}
        {%- endfor -%}'
        }
    }],

    credits: {
      enabled: false,
      href: "https://github.com/kizniche/Mycodo",
      text: "Mycodo"
    }
  });
"""
}