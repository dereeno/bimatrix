$(document).ready(function() {

  create_matrix(2,2);

  $('form.dimensions').on('submit', function() {
    m = $('input#number_m').val();
    n = $('input#number_n').val();

    if (validate_less_then_9(m,n)){
      create_matrix(m,n);
    }

  });

  $('form#bimatrix .random').on('click', function(){
    $.each($('form#bimatrix').find(':input:not([type=hidden])'), function(index, input){
      rand = Math.floor(Math.random() * 10) + 1
      $(input).val(rand);
    })
    return false;
  })

  $('form#bimatrix').on('submit', function() {
    rows = $(this).find('input[name="hidden_m"]').val()
    cols = $(this).find('input[name="hidden_n"]').val()
    var matrices = collect_matrix(parseInt(rows),parseInt(cols));
    $(".overlay").show();
    $.ajax({
      type: "POST",
      url: "/",
      data : {
        'A': JSON.stringify(matrices[0]), 'B': JSON.stringify(matrices[1]),
        'm': rows, 'n': cols
      },
      success: function(results) {
        // console.log(results);
        build_equilbria_table(results['equilibria'])
        show_results(results['components']);
      },
      error: function(error) {
        console.log(error)
      }

    });

    $(".overlay").hide();

    function build_equilbria_table(equilibria){
      eq_table = $('#eq-table tbody')[0]
      eq_table.innerHTML = '';
      $.each(equilibria, function(i, eq){
        row = document.createElement('tr');
        eq_table.appendChild(row);
        number = document.createElement('td');
        st1 = document.createElement('td');
        pay1 = document.createElement('td');
        st2 = document.createElement('td');
        pay2 = document.createElement('td');

        row.appendChild(number);
        row.appendChild(st1);
        row.appendChild(pay1);
        row.appendChild(st2);
        row.appendChild(pay2);
        number.innerHTML = i+1;
        st1.innerHTML = eq[0]['distribution'];
        st2.innerHTML = eq[1]['distribution'];
        pay1.innerHTML = eq[0]['payoff'];
        pay2.innerHTML = eq[1]['payoff'];
      })

    }

    function show_results(results){
      // comp_table =document.getElementById('comp-table');
      comp_table = $('#comp-table tbody')[0]
      comp_table.innerHTML = '';
      $.each(results, function(i, comp_value){
        row = document.createElement('tr');
        cell = document.createElement('td');
        cell.innerHTML = i+1;
        row.appendChild(cell);
        comp_table.appendChild(row);
        eq_cell = document.createElement('td');
        row.appendChild(eq_cell);
          $.each(comp_value, function(eq_name, eq_value){
            if (eq_name == 'index'){
              index_cell = document.createElement('td')
              index_cell.innerHTML = "index: " + eq_value;
              row.appendChild(index_cell);
            }
            else{
              eq_row = document.createElement('tr');
              cell1 = document.createElement('td');
              cell2 = document.createElement('td');
              cell3 = document.createElement('td');
              cell2.innerHTML = ", x: [" + eq_value['x']+']';
              cell3.innerHTML = ", y: [" + eq_value['y']+']';
              cell1.innerHTML = "lex-index: " + eq_value['lexindex'];
              eq_row.appendChild(cell1);
              eq_row.appendChild(cell2);
              eq_row.appendChild(cell3);
              eq_cell.appendChild(eq_row);
            }
          })
      })
    }

    function collect_matrix(rows,cols) {
        var A_values = [];
        var B_values = [];
        var form = $('form#bimatrix');
        for (var i = 0; i < rows; i++){
          A_values.push([]);
          B_values.push([]);
          for(var j = 0; j < cols; j++){
            A_values[i].push(form.find('input[row='+i+'][col='+j+'].A_entry').val());
            B_values[i].push(form.find('input[row='+i+'][col='+j+'].B_entry').val());
          }
        }
      return [A_values,B_values];
    };
  });

  function validate_less_then_9(m,n){
    if (m > 9 || n > 9 || m < 0 || n < 0 ){
      alert('value must be less then 9');
      return false
    }
    return true;
  }

  function create_matrix(rows, cols){
    var d = document.createElement('td'),
        bimatrix=document.getElementById('table');
    d.className='cell';

    bimatrix.innerHTML = "";
    for(var i=0;i<rows;i++){
        row = document.createElement('tr');
      for(var j=0;j<cols;j++){
          var c=d.cloneNode(false);
          var inp1 = document.createElement('input');
          inp1.setAttribute('row', i);
          inp1.setAttribute('col', j);
          inp1.setAttribute('required','true');
          inp1.setAttribute('type', 'number');
          var inp2 = inp1.cloneNode(false);
          inp1.className =  "A_entry";
          inp2.className =  "B_entry";
          c.appendChild(inp1);
          c.appendChild(inp2);
          row.appendChild(c);
      }
      bimatrix.appendChild(row);
    }
    $('form#bimatrix input[name="hidden_m"]').val(rows);
    $('form#bimatrix input[name="hidden_n"]').val(cols);

  };

});