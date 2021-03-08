// toggle sintomas
function funcDisable(myId1,myId2) {
    var x = document.getElementById(myId1);
    document.getElementById(myId2).disabled = !(document.getElementById(myId1).checked);
    if ( document.getElementById(myId2).disabled){
      document.getElementById(myId2).value = '';
      document.getElementById(myId2).placeholder = '';
    }
    else{ 
      document.getElementById(myId2).placeholder = 'Há quantos dias?';
      document.getElementById('semsin').checked = false;
    }
  }
  
  // validação dos campos de dias dos sintomas quando check true
  function funcTemDias(myId1,myId2, frase) {
    if(document.getElementById(myId1).checked && document.getElementById(myId2).value == ''){
        alert(frase);
        document.getElementById(myId2).focus();
        return false
    }
    else
      return true
  }
  
  // validação do Form
  function validateForm() {
  
    //idade
    if(document.getElementById('idade').value =='' ) 
    { 
      alert('O campo idade deve ser preenchido.');
      document.getElementById('idade').focus();
      return false
    }
    if(isNaN(document.getElementById('idade').value) ) 
    { 
      alert('O campo idade deve ser preenchido com um valor numérico');
      document.getElementById('idade').value = '';
      document.getElementById('idade').focus();
      return false    
    }
    else
    {
      if(!(isNaN(document.getElementById('idade').value))) {
        if(parseInt(document.getElementById('idade').value) < 0 )
          {
              alert('O campo Idade deve ter valor válido.');
              document.getElementById('idade').value = '';
              document.getElementById('idade').focus();
              return false    
          }
      }
    }
  
    // genero
    if(document.getElementById('genero').value=='-') 
    { 
      alert('O campo gênero deve ser preenchido.');
      document.getElementById('genero').focus();
      return false
    }
    if (!(checksin())){
      alert('"Caso não possua os sintomas marque: "Não tenho nenhuma dos sintomas"');
      document.getElementById('semsin').focus();
      return false;
    }
  
    // febre
    if(document.getElementById('bfebre').checked && isNaN(document.getElementById('febre').value)) 
    { 
      alert('O campo da Febre deve ser numérico.');
      document.getElementById('febre').value = '';
      document.getElementById('febre').focus();
      return false
    }
    else
    {
      if(!(isNaN(document.getElementById('febre').value))) {
        if(parseInt(document.getElementById('febre').value) < 0 )
          {
              alert('O campo da Febre deve ter valor válido.');
              document.getElementById('febre').value = '';
              document.getElementById('febre').focus();
              return false    
          }
      }
    }
  
    // tosse
    if( document.getElementById('btosse').checked  && isNaN(document.getElementById('tosse').value)) 
    { 
      alert('O campo da Tosse deve ser numérico.');
      document.getElementById('tosse').value = '';
      document.getElementById('tosse').focus();
      return false
    }
    else
    {
      if(!(isNaN(document.getElementById('tosse').value))) {
        if(parseInt(document.getElementById('tosse').value) < 0 )
          {
              alert('O campo da Tosse deve ter valor válido.');
              document.getElementById('tosse').value = '';
              document.getElementById('tosse').focus();
              return false    
          }
      }
    }
  
    // dor de garganta
    if(document.getElementById('bdorDeGarganta').checked && isNaN(document.getElementById('dorDeGarganta').value))
    {
      alert('O campo da Dor de garganta deve ser numérico.');
      document.getElementById('dorDeGarganta').value = '';
      document.getElementById('dorDeGarganta').focus();
      return false
    }
    else
    {
      if(!(isNaN(document.getElementById('dorDeGarganta').value))) {
        if(parseInt(document.getElementById('dorDeGarganta').value) < 0 )
          {
              alert('O campo da Dor de garganta deve ter valor válido.');
              document.getElementById('dorDeGarganta').value = '';
              document.getElementById('dorDeGarganta').focus();
              return false    
          }
      }
    }
  
    // coriza
    if(document.getElementById('bcoriza').checked && isNaN(document.getElementById('coriza').value)) 
    { 
      alert('O campo da Coriza deve ser numérico.');
      document.getElementById('coriza').value = '';
      document.getElementById('coriza').focus();
      return false
    }
    else
    {
      if(!(isNaN(document.getElementById('coriza').value))) {
        if(parseInt(document.getElementById('coriza').value) < 0 )
          {
              alert('O campo Coriza deve ter valor válido.');
              document.getElementById('coriza').value = '';
              document.getElementById('coriza').focus();
              return false    
          }
      }
    }
  
    // febre
    var dias  = funcTemDias('bfebre','febre','Favor informar o número de dias de Febre.');
    if (!(dias)) return false
  
    var dias  = funcTemDias('btosse','tosse','Favor informar o número de dias de Tosse.');
    if (!(dias)) return false
  
    var dias  = funcTemDias('bdorDeGarganta','dorDeGarganta','Favor informar o número de dias de Dor de garganta.');
    if (!(dias)) return false
  
    var dias  = funcTemDias('bcoriza','coriza','Favor informar o número de dias de Coriza.');
    if (!(dias)) return false
    
    var option=document.getElementsByName('faltaDeAr');
    if(!(option[0].checked || option[1].checked)) 
    { 
      alert('O campo Falta de ar deve ser selecionado.');
      option[0].focus();
      return false
    }
    
    // sem enfermidades
    if (!(checkenfer())){
      alert('"Caso não possua as enfermidades marque: "Não tenho nenhuma das enfermidades"');
      document.getElementById('semenfer').focus();
      return false;
    }
  
    // frases
    var f1 = document.getElementById("oFrase1").innerText ;
    var f2 = document.getElementById("oFrase2").innerText ;
    var f3 = document.getElementById("oFrase3").innerText ;
    if ( f1 == "Grave a frase 1" || f2 == "Grave a frase 2" || f3 == "Grave a frase 3") {
      alert("Grave todas as Frases clicando nos botões.");
      return false;
    }
    return true
  }
  
  // reseta os checks/inputs de sintaomas
  function gosemsin() {
    document.getElementById('bfebre').checked = false;
    document.getElementById('btosse').checked = false;
    document.getElementById('bdorDeGarganta').checked = false;
    document.getElementById('bcoriza').checked = false;
    document.getElementById('febre').value = "";
    document.getElementById('tosse').value = "";
    document.getElementById('dorDeGarganta').value = "";
    document.getElementById('coriza').value = "";
    document.getElementById('febre').disabled = true;
    document.getElementById('tosse').disabled = true;
    document.getElementById('dorDeGarganta').disabled = true;
    document.getElementById('coriza').disabled = true;
    document.getElementById('febre').placeholder = "";
    document.getElementById('tosse').placeholder = "";
    document.getElementById('dorDeGarganta').placeholder = "";
    document.getElementById('coriza').placeholder = "";
  }
  
  // reseta os checks/inputs de sintomas
  function gosemenfer(){
    document.getElementById('doencaCronicaPulmao').checked = false;
    document.getElementById('doencaCoroniana').checked = false;
    document.getElementById('pressaoAlta').checked = false;
    document.getElementById('diabetes').checked = false;
  }
  
  // reseta sem enfermidade
  function clearSemEnfer(){
    document.getElementById('semenfer').checked = false;  
  }
  
  // checa se algum sintoma foi selecionado
  function checksin(){
    var feb = document.getElementById('bfebre').checked;
    var tos = document.getElementById('btosse').checked;
    var dor = document.getElementById('bdorDeGarganta').checked;
    var cor = document.getElementById('bcoriza').checked;
    var sem = document.getElementById('semsin').checked;
    if (!(feb || tos || dor || cor || sem)) {
      return false
    }
      else return true
  }
  
  // checa se alguma enfermidade foi seleciada
  function checkenfer(){
    var cro = document.getElementById('doencaCronicaPulmao').checked;
    var cor = document.getElementById('doencaCoroniana').checked;
    var pre = document.getElementById('pressaoAlta').checked;
    var dia = document.getElementById('diabetes').checked;
    var sem = document.getElementById('semenfer').checked;
    if (!(cro || cor || pre || dia || sem)) {
      return false
    }
      else return true
  }
  
  // pega valor de cookie
  function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }