  const app = new Clarifai.App({apiKey: 'bb5f7ed42b944db7b8cdf566b13c67a6'});

            document.getElementById('pred').onclick=function(e){
                
            var file=document.querySelector('input[type=file]').files[0];
           // var file    = document.querySelector("input[type=file]").files[0]; 
            var reader  = new FileReader();
            console.log(file);
            reader.addEventListener("load", function () {
                var localBase64 = reader.result.split("base64,")[1]; 
                dopred({ base64: localBase64 });  
                }, false);
            if (file) {
                reader.readAsDataURL(file);
                    }
                };

            function dopred(value){
            app.models.predict(Clarifai.GENERAL_MODEL,value).then(
            function(response) {
                    if(response.rawData.outputs[0].data.hasOwnProperty("concepts")) {
                        tagArray = response.rawData.outputs[0].data.concepts;
                        conceptNames='';
                        for (var other = 0; other < tagArray.length; other++) {
                        console.log(tagArray[other]); 
                        conceptNames += '<li>' + tagArray[other].name + ': <i>' + tagArray[other].value + '</i></li>';
                        }
                        document.getElementById("outp").innerHTML=conceptNames;
                        }
                        
                },
                function(err) {
                    alert(err);
                }   
                );
            }   