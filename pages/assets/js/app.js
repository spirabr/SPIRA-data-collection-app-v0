
//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
//var pauseButton = document.getElementById("pauseButton");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
//pauseButton.addEventListener("click", pauseRecording);

function startRecording() {
	
	console.log("recordButton clicked");

	/*
		Simple constraints object, for more advanced audio features see
		https://addpipe.com/blog/audio-constraints-getusermedia/
	*/
    
    var constraints = { audio: true, video:false }

 	/*
    	Disable the record button until we get a success or fail from getUserMedia() 
	*/

	recordButton.disabled = true;
	stopButton.disabled = false;
	//pauseButton.disabled = false
	$("#btnR2").css("display", "none");
	$("#mic2").css("display", "block");
	$('h3#P21').text('Gravando...');
	$('h3#P22').text('Agora leia a frase:');
	$('h3#P23').text('Já leu? Clique em:');
	/*
    	We're using the standard promise based getUserMedia() 
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

		/*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device

		*/
		audioContext = new AudioContext();

		//update the format 
		//document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"

		/*  assign to gumStream for later use  */
		gumStream = stream;
		
		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);

		/* 
			Create the Recorder object and configure to record mono sound (1 channel)
			Recording 2 channels  will double the file size
		*/
		rec = new Recorder(input,{numChannels:1})

		//start the recording process
		rec.record()

		console.log("Recording started");

	}).catch(function(err) {
	  	//enable the record button if getUserMedia() fails
    	recordButton.disabled = false;
		stopButton.disabled = true;
		
    	//pauseButton.disabled = true
	});
}


function stopRecording() {
	console.log("stopButton clicked-----");

	//disable the stop button, enable the record too allow for new recordings
	//recordButton.innerHTML = "Analisando..."
	//stopButton.disabled = true;
	recordButton.disabled = false;
	//pauseButton.disabled = true;
	$("#mic").css("display", "none");
	$('h3#P31').css("display", "none");
	$('h3#P32').css("display", "none");
	$('h3#P33').css("display", "none");
	$('h2#F31').css("display", "none");

	//reset button just in case the recording is stopped while paused
	//pauseButton.innerHTML="Pause";
	
	//tell the recorder to stop the recording
	rec.stop();
	//wait(1000);

	//stop microphone access
	gumStream.getAudioTracks()[0].stop();
	//wait(1000);

	//create the wav blob and pass it on to createDownloadLink
	rec.exportWAV(createDownloadLink);
	
}

function createDownloadLink(blob) {

	var xhr=new XMLHttpRequest();
	xhr.onload=function(e) {
		if(this.readyState === 4) {
			console.log("Server returned: ",e.target.responseText);
		}
	};
	var fd=new FormData();
	fd.append("audio_data",blob, 'temp.wav');
	fd.append( "id",fraseN);
	xhr.open("POST","uploader",true);  
	xhr.onprogress = function (e) {
	if (e.lengthComputable) {
		console.log(e.loaded+  " / " + e.total)
	}
	}
	xhr.onloadstart = function (e) {
		console.log("start")
		nextStepdButton2.disabled = true;
		$("#mic3").css("display", "block");
		$("#myModal2").modal("hide");
		$("#myModal3").modal("show");
		$('h2#F31').css("display", "block");
		$('h2#F31').text("Enviando Voz...");
		//$('button#stopButton').css("display", "none");
	}
	xhr.onloadend = function (e) {
		console.log("end");
		resetModal2();
		$("#mic3").css("display", "none");
		$('h2#F31').text("Voz enviada com sucesso.");
		nextStepdButton2.disabled = false;
		document.getElementById("oFrase" + fraseN).innerHTML = "Frase " + fraseN + ": gravada"
		

	}
	xhr.send(fd);
		  
}

// Reseta o Modal ao estado original para próxima gravação
function resetModal2(){
	$("#btnR2").css("display", "block");
	document.getElementById("P21").innerHTML = "<b>Passo 1</b> Fale próximo ao microfone e sem usar viva voz clique no botão:</h3>";
	recordButton.disabled = false;
	$("#mic2").css("display", "none");                  
	document.getElementById("P22").innerHTML = "";
	document.getElementById("P23").innerHTML = "<b>Passo 3</b> Clique no botão:</h3>";
	document.getElementById("F2").innerHTML = "";
	stopButton.disabled = true;
	nextStepdButton2.disabled = true;
}
