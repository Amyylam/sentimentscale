var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition
var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList
var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent

//var colors = [ 'chicken', 'tomato', 'egg','onion','garlic','celery','beef','pork'];
//var grammar = '#JSGF V1.0; grammar colors; public <color> = ' + colors.join(' | ') + ' ;'

var recognition = new SpeechRecognition();
//var speechRecognitionList = new SpeechGrammarList();
//speechRecognitionList.addFromString(grammar, 1);
//recognition.grammars = speechRecognitionList;
recognition.continuous = false;
recognition.lang = 'en-US';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

var recognition2 = new SpeechRecognition();
//recognition2.grammars = speechRecognitionList;
recognition2.continuous = false;
recognition2.lang = 'en-US';
recognition2.interimResults = false;
recognition2.maxAlternatives = 1;


var diagnostic = document.querySelector('.output');
var bg = document.querySelector('html');
//var hints = document.querySelector('.hints');
var Q1 = document.querySelector('.Q1');
var Q2 = document.querySelector('.Q2');
//var output2 = document.querySelector('.output2');
var liked_box = document.querySelector('#liked_ingredients');
var disliked_box = document.querySelector('#disliked_ingredients');

var liked = '';
var disliked = '';
var maintext = document.getElementById("maintext");


//var recipes = ['crispy crunchy  chicken','george s at the cove  black bean soup'];

function add_recipes(){
    var recipes_array = [];
    var recipes =  document.getElementById("recipetext").textContent.split(", ");
    recipes.forEach(function(entry){
      recipes_array.push(entry);
    });
    console.log(recipes_array);

    var recipe_options_html = "<form id='recipe' action='/'><label for='recipe_options'>Choose a recipe:</label><select id='recipe_options' onchange='submit_recipe();'>";
    function myFunction(item,index) {
        recipe_options_html += "<option value='"+item+"'>"+item+"</option>";
        //console.log("<option value='"+item+"'>"+item+"</option>");
    };

    recipes_array.forEach(myFunction);
    recipe_options_html += "</select></form>";
    console.log(recipe_options_html);
    recipetext.innerHTML = recipe_options_html;

    

}



//document.body.onclick = function() {
//  recognition.start();
//  console.log('Ready to receive a color command.');
//}

liked_box.onclick = function() {
  recognition.start();
  console.log('Ready to receive a color command.');
}

disliked_box.onclick = function() {
  recognition2.start();
  console.log('Ready to receive a color command.');
}

recognition.onresult = function(event) {
  // The SpeechRecognitionEvent results property returns a SpeechRecognitionResultList object
  // The SpeechRecognitionResultList object contains SpeechRecognitionResult objects.
  // It has a getter so it can be accessed like an array
  // The first [0] returns the SpeechRecognitionResult at the last position.
  // Each SpeechRecognitionResult object contains SpeechRecognitionAlternative objects that contain individual results.
  // These also have getters so they can be accessed like arrays.
  // The second [0] returns the SpeechRecognitionAlternative at position 0.
  // We then return the transcript property of the SpeechRecognitionAlternative object
  var color = event.results[0][0].transcript;
  liked_box.value = 'Result received: ' + color + '.';
  liked = color;
  console.log('Confidence: ' + event.results[0][0].confidence);
}

recognition2.onresult = function(event) {
  var color = event.results[0][0].transcript;
  disliked_box.value = 'Result received: ' + color + '.';
  disliked = color;
  //output2.textContent = liked + " " + disliked
  console.log('Confidence: ' + event.results[0][0].confidence);
}

recognition.onspeechend = function() {
  recognition.stop();
}

recognition.onnomatch = function(event) {
  diagnostic.textContent = "I didn't recognise that liked ingredient(s).";
}

recognition.onerror = function(event) {
  diagnostic.textContent = 'Error occurred in recognition: ' + event.error;
}

recognition2.onspeechend = function() {
  recognition2.stop();
}

recognition2.onnomatch = function(event) {
  diagnostic.textContent = "I didn't recognise that disliked ingredient(s).";
}

recognition2.onerror = function(event) {
  diagnostic.textContent = 'Error occurred in recognition: ' + event.error;
}

function update_page(response) {
	var div = document.getElementById("maintext");
	div.innerHTML = response;
        //var bg = document.querySelector('html');
        //bg.innerHTML = response;

}

function update_recipe_list(response) {
	var div = document.getElementById("recipetext");
	div.innerHTML = response;


}

function submit_form() {   
        var queryString = "liked="+liked+"&disliked="+disliked

	xmlHttpRqst = new XMLHttpRequest();
	xmlHttpRqst.onload = function(e) {update_recipe_list(xmlHttpRqst.response);} 
	xmlHttpRqst.open("GET", "/?"+queryString);
	xmlHttpRqst.send();

}

function submit_recipe() {   
        var selected_recipe = document.getElementById("recipe_options");
        selected_recipe_value = selected_recipe.value;
        console.log(selected_recipe_value);
        var queryString = encodeURI("recipe="+selected_recipe_value);
        console.log(queryString);


	xmlHttpRqst2 = new XMLHttpRequest();
	xmlHttpRqst2.onload = function(e) {update_page(xmlHttpRqst2.response);} 
	xmlHttpRqst2.open("GET", "/?"+queryString);
	xmlHttpRqst2.send();

}