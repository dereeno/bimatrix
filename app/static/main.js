$(document).ready(function() {
  console.log("ready!");

  // on form submission ...
  $('form.dimensions').on('submit', function() {

    console.log("the form has beeen submitted");

    // grab values
    m = $('input#number_m').val();
    n = $('input#number_n').val();
    create_matrix(m,n);

    });
  // Creating variables

  $('form#wrapper').on('submit', function() {

    console.log('hi there!');
    rows = $(this).find('input[name="hidden_m"]').val()
    cols = $(this).find('input[name="hidden_n"]').val()
    var matrices = collect_matrix(parseInt(rows),parseInt(cols));

    $.ajax({
      type: "POST",
      url: "/",
      data : {
        'A': JSON.stringify(matrices[0]), 'B': JSON.stringify(matrices[1]),
        'm': m, 'n': n
      },
      success: function(results) {
        console.log(results);
        show_results(results);
      },
      error: function(error) {
        console.log(error)
      }
    });

    function show_results(results){
      $.each(results, function(comp_name, comp_value){
        console.log(comp_name);
          $.each(comp_value, function(eq_name, eq_value){
            if (eq_name == 'index'){
              console.log("index is " + eq_value);
            }
            else{
              console.log("lex " + eq_value['lexindex']);
              console.log("x " + eq_value['x']);
              console.log("y " + eq_value['y']);
            }
          })
      })
    }

    function collect_matrix(rows,cols) {
        var myArr = document.forms.wrapper;
        var myControls = myArr;
        var name_value_array = [];
        var A_values = [];
        var B_values = [];
        var form = $('form#wrapper');
        for (var i = 0; i < rows; i++){
          A_values.push([]);
          B_values.push([]);
          for(var j = 0; j < cols; j++){
            A_values[i].push(form.find('input[row='+i+'][col='+j+'].A_entry').val());
            B_values[i].push(form.find('input[row='+i+'][col='+j+'].B_entry').val());
          }
        }


        // for (var i = 0; i < myControls.length; i++) {
        //   var aControl = myControls[i];
        //   if (aControl.type != "button") {
        //     // store value in a map
        //     name_value_array.push(aControl.value, aControl.name);
        //     // document.getElementById("resultField").appendChild(document.createTextNode(aControl.value + " "));
        //   }

        // }
        // show map values as a popup
        console.log("A");
        console.log(A_values);
        console.log("B");
        console.log(B_values);
      return [A_values,B_values];
    };



  });

  function create_matrix(rows, cols){
    var wid=100,
        hei=100,
        d=document.createElement('div'),
        input1 = document.createElement('input'),
        wrap=document.getElementById('wrapper');
    d.className='cell';
    d.style.width=wid+'px';
    d.style.height=hei+'px';
    input1.setAttribute('type', 'number');
    //Creating elements
    wrap.innerHTML = "";
    for(var i=0;i<rows;i++){
      for(var j=0;j<cols;j++){
          var c=d.cloneNode(false);
          var inp1 = input1.cloneNode(false);
          inp1.setAttribute('row', i);
          inp1.setAttribute('col', j);
          inp1.setAttribute('required','true');
          var inp2 = inp1.cloneNode(false);
          inp1.className =  "A_entry";
          inp2.className =  "B_entry";
          c.appendChild(inp1);
          c.appendChild(inp2);
          wrap.appendChild(c);
    }}

    //Setting position
    for(var i=0;i<wrap.childNodes.length;i++){
        setCSS(i);
    }

    var btn = document.createElement('button');
    btn.setAttribute('type', 'submit');
    btn.className = "btn btn-default run_algo"
    btn.innerHTML = "GO!"
    wrap.appendChild(btn);

    var hidden_input_m = document.createElement("input");
    var hidden_input_n = document.createElement("input");
    hidden_input_m.setAttribute("type", "hidden");
    hidden_input_n.setAttribute("type", "hidden");
    hidden_input_m.setAttribute("name", "hidden_m");
    hidden_input_n.setAttribute("name", "hidden_n");
    hidden_input_m.setAttribute("value", rows);
    hidden_input_n.setAttribute("value", cols);

    wrap.appendChild(hidden_input_m);
    wrap.appendChild(hidden_input_n);

    function setCSS(i){
      var el=wrap.childNodes[i];
      el.style.top=Math.floor(i/cols)*hei+'px';
      el.style.left=i%cols*wid+'px';
    }
  };





});