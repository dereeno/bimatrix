$(document).ready ->

  setAttributes = (el, attrs) ->
    for key, value of attrs
      el.setAttribute(key, value)

  create_matrix = (rows, cols) ->
    toClone = document.createElement('td')
    toClone.className = 'cell'
    bimatrix = document.getElementById('bimatrix-table')
    bimatrix.innerHTML = ''
    i = 0
    while i < rows
      row = document.createElement('tr')
      j = 0
      while j < cols
        cell = toClone.cloneNode()
        inp1 = document.createElement('input')
        setAttributes inp1,
          'row': i
          'col': j
          'required': 'true'
          'type': 'number'
          'min': '0'
        inp2 = inp1.cloneNode()
        inp1.className = 'A_entry'
        inp2.className = 'B_entry'
        cell.appendChild(inp1).className = 'A_entry'
        cell.appendChild(inp2).className = 'B_entry'
        row.appendChild cell
        j++
      bimatrix.appendChild row
      i++
    $('form#bimatrix-form input[name="hidden_m"]').val rows
    $('form#bimatrix-form input[name="hidden_n"]').val cols
    return

  create_matrix 2, 2

  $('form.dimensions').on 'submit', ->
    m = $('input#number_m').val()
    n = $('input#number_n').val()
    create_matrix m, n

  $('form.dimensions input').on 'focus', ->
    $(this).val('')

  $('form#bimatrix-form .random').on 'click', ->
    $.each $('form#bimatrix-form').find(':input:not([type=hidden])'), (index, input) ->
      rand = Math.floor(Math.random() * 10) + 1
      $(input).val rand

  $('form#bimatrix-form .clear').on 'click', ->
    $('form#bimatrix-form').find(':input:not([type=hidden])').val('')

  $('form#bimatrix-form').on 'submit', ->
    $('.results').hide()
    build_equilbria_table = (equilibria) ->
      eq_table = $('#eq-table tbody')[0]
      eq_table.innerHTML = ''

      $.each equilibria, (i, eq) ->
        row = document.createElement('tr')
        eq_table.appendChild row
        (row.appendChild document.createElement('td')).innerHTML = i + 1
        (row.appendChild document.createElement('td')).innerHTML = 'x<sup>' + eq[0]['number'] + '</sup>'
        (row.appendChild document.createElement('td')).innerHTML = '[' + eq[0]['distribution'].join(', ') + ']'
        (row.appendChild document.createElement('td')).innerHTML = eq[0]['payoff']
        (row.appendChild document.createElement('td')).innerHTML = 'y<sup>' + eq[1]['number'] + '</sup>'
        (row.appendChild document.createElement('td')).innerHTML = '[' + eq[1]['distribution'].join(', ') + ']'
        (row.appendChild document.createElement('td')).innerHTML = eq[1]['payoff']

    build_components_table = (results) ->
      comp_table = $('#comp-table tbody')[0]
      comp_table.innerHTML = ''

      $.each results, (i, comp_value) ->

        row = document.createElement('tr')
        comp_table.appendChild row

        number_cell = document.createElement('td')
        number_cell.innerHTML = i + 1
        subsets = comp_value['nash_subsets']
        equilibria = comp_value['equilibria']

        subsets_cell = document.createElement('td')
        subsets_cell.setAttribute('colspan', 3)
        subsets_cell.className = 'subsets-cell'
        subsets_table = document.createElement('table')
        subsets_table.className = 'small-table subsets'
        subsets_cell.appendChild subsets_table
        subsets_tbody = document.createElement('tbody')
        subsets_table.appendChild subsets_tbody

        equilibria_cell = document.createElement('td')
        equilibria_cell.setAttribute('colspan', 2)
        equilibria_cell.className = 'equilibria-cell'
        equilibria_table = document.createElement('table')
        equilibria_cell.appendChild equilibria_table
        equilibria_table.className = 'small-table'
        equilibria_tbody = document.createElement('tbody')
        equilibria_table.appendChild equilibria_tbody

        for subset in subsets
          current_row = document.createElement('tr')
          current_row.appendChild parse_component('x', subset[0])
          cell = document.createElement('td')
          cell.className = 'central'
          cell.innerHTML = 'X'
          current_row.appendChild cell
          current_row.appendChild parse_component('y', subset[1])
          subsets_tbody.appendChild current_row

        for eq in equilibria
          current_row = document.createElement('tr')
          cell1 = document.createElement('td')
          cell2 = document.createElement('td')
          cell1.className = 'x'
          cell2.className = 'y'
          cell1.innerHTML = eq['eq_number']
          cell2.innerHTML = eq['lex_index']
          current_row.appendChild cell1
          current_row.appendChild cell2
          equilibria_tbody.appendChild current_row

        index_cell = document.createElement('td')
        index_cell.innerHTML = comp_value['index']
        row.appendChild index_cell

        append_children row, [number_cell, subsets_cell, equilibria_cell, index_cell]

    append_children = (parent, children) ->
      for child in children
        parent.appendChild(child)

    parse_component = (player, strategies) ->
      text = '{ '
      for i in strategies
        text += player + '<sup>' + i + '</sup>' + ", "

      text = text.slice(0, -2) + ' }'
      result = document.createElement('td')
      result.className = player
      result.innerHTML = text
      return result


    collect_matrix_data = (rows, cols) ->
      A_values = []
      B_values = []
      form = $('form#bimatrix-form')
      i = 0
      while i < rows
        A_values.push []
        B_values.push []
        j = 0
        while j < cols
          A_values[i].push form.find('input[row=' + i + '][col=' + j + '].A_entry').val()
          B_values[i].push form.find('input[row=' + i + '][col=' + j + '].B_entry').val()
          j++
        i++
      [A_values, B_values]

    rows = $(this).find('input[name="hidden_m"]').val()
    cols = $(this).find('input[name="hidden_n"]').val()
    matrices = collect_matrix_data(parseInt(rows), parseInt(cols))

    $.ajax
      type: 'POST'
      url: '/'
      data:
        'A': JSON.stringify(matrices[0])
        'B': JSON.stringify(matrices[1])
        'm': rows
        'n': cols
      success: (results) ->
        build_equilbria_table results['equilibria']
        build_components_table results['components']
        $('.results').fadeIn()
      error: (error) ->
        console.log error

  timer = null
  $(document).ajaxStart ->
    if timer then clearTimeout(timer)
    timer = setTimeout((-> $('body').addClass 'loading'), 500)
  $(document).ajaxComplete ->
    clearTimeout(timer)
    $('body').removeClass 'loading'
