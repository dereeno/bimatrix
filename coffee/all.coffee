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
    $('.results').hide()
    $.each $('form#bimatrix-form').find(':input:not([type=hidden])'), (index, input) ->
      rand = Math.floor(Math.random() * 10) + 1
      $(input).val rand

  $('form#bimatrix-form .clear').on 'click', ->
    $('.results').hide()
    $('form#bimatrix-form').find(':input:not([type=hidden])').val('')

  $('form#bimatrix-form').on 'submit', ->
    $('.results').hide()
    build_equilbria_table = (equilibria) ->
      eq_table = $('#eq-table tbody')[0]
      eq_table.innerHTML = ''

      $.each equilibria, (i, eq) ->
        row = document.createElement('tr')
        eq_table.appendChild row
        number = document.createElement('td')
        st1 = document.createElement('td')
        pay1 = document.createElement('td')
        st2 = document.createElement('td')
        pay2 = document.createElement('td')
        row.appendChild number
        row.appendChild st1
        row.appendChild pay1
        row.appendChild st2
        row.appendChild pay2
        number.innerHTML = i + 1
        st1.innerHTML = '[ ' + eq[0]['distribution'].join(', ') + ' ]'
        st2.innerHTML = '[ ' + eq[1]['distribution'].join(', ') + ' ]'
        pay1.innerHTML = eq[0]['payoff']
        pay2.innerHTML = eq[1]['payoff']
      return

    build_components_table = (results) ->
      comp_table = $('#comp-table tbody')[0]
      comp_table.innerHTML = ''

      $.each results, (i, comp_value) ->
        row = document.createElement('tr')
        cell_comp_number = document.createElement('td')
        cell_comp_number.innerHTML = i + 1
        row.appendChild cell_comp_number
        comp_table.appendChild row
        eq_cell = document.createElement('td')
        eq_cell.className = 'small-eq-table'
        row.appendChild eq_cell
        table = document.createElement('table')
        table.className = 'table'
        eq_cell.appendChild(table)
        thead = document.createElement('thead')
        table.appendChild(thead)
        number_header = document.createElement('th')
        number_header.innerHTML = 'number'
        thead.appendChild(number_header)
        lex_index_header = document.createElement('th')
        lex_index_header.innerHTML = 'lex-index'
        thead.appendChild(lex_index_header)
        tbody = document.createElement('tbody')
        table.appendChild(tbody)

        $.each comp_value['equilibria'], (j, eq_hash) ->
          eq_row = document.createElement('tr')
          cell1 = document.createElement('td')
          cell2 = document.createElement('td')
          cell1.innerHTML = eq_hash['eq_number']
          cell2.innerHTML = eq_hash['lex_index']
          eq_row.appendChild cell1
          eq_row.appendChild cell2
          tbody.appendChild eq_row

        index_cell = document.createElement('td')
        index_cell.innerHTML = comp_value['index']
        row.appendChild index_cell

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
        $('.results').show()
      error: (error) ->
        console.log error

  $(document).ajaxStart ->
    $('body').addClass 'loading'
  $(document).ajaxComplete ->
    $('body').removeClass 'loading'
