// ===============================
// Universal ID Studio
// Template Designer
// Part 1
// ===============================



// Status

function setStatus(msg){

    document.getElementById("status").innerHTML = msg;

}

// ----------------------------
// Upload Template
// ----------------------------

document
.getElementById("uploadTemplate")
.onclick = function(){

    document
    .getElementById("templateFile")
    .click();

};

document
.getElementById("templateFile")
.onchange = function(e){

    const file = e.target.files[0];

    if(!file)
        return;

    const reader = new FileReader();

    reader.onload = function(f){

        fabric.Image.fromURL(

            f.target.result,

            function(img){

                canvas.clear();

                canvas.setBackgroundImage(

                    img,

                    canvas.renderAll.bind(canvas),

                    {

                        scaleX:
                        canvas.width /
                        img.width,

                        scaleY:
                        canvas.height /
                        img.height

                    }

                );

                setStatus(
                    "Template Loaded Successfully"
                );

            }

        );

    };

    reader.readAsDataURL(file);

};

// ---------------------------------
// Add Photo Placeholder
// ---------------------------------

document
.getElementById("addPhoto")
.onclick = function(){

    let rect = new fabric.Rect({

        left:40,

        top:50,

        width:160,

        height:200,

        fill:"rgba(0,0,255,0.20)",

        stroke:"blue",

        strokeWidth:2,

        name:"photo"

    });

    canvas.add(rect);

    canvas.setActiveObject(rect);

    setStatus("Photo Placeholder Added");

};

// ======================================
// Add Name
// ======================================

document
.getElementById("addName")
.onclick = function(){

    let text = new fabric.Text("Student Name",{

        left:260,
        top:60,
        fontSize:28,
        fill:"black",
        fontFamily:"Arial",
        name:"name"

    });

    canvas.add(text);

    canvas.setActiveObject(text);

    setStatus("Name Field Added");

};

// ======================================
// Add Roll Number
// ======================================

document
.getElementById("addRoll")
.onclick = function(){

    let text = new fabric.Text("Roll Number",{

        left:260,
        top:120,
        fontSize:28,
        fill:"black",
        fontFamily:"Arial",
        name:"roll"

    });

    canvas.add(text);

    canvas.setActiveObject(text);

    setStatus("Roll Number Field Added");

};

// ======================================
// Add Branch
// ======================================

document
.getElementById("addBranch")
.onclick = function(){

    let text = new fabric.Text("Branch",{

        left:260,
        top:180,
        fontSize:28,
        fill:"black",
        fontFamily:"Arial",
        name:"branch"

    });

    canvas.add(text);

    canvas.setActiveObject(text);

    setStatus("Branch Field Added");

};

// ======================================
// Add Year
// ======================================

document
.getElementById("addYear")
.onclick = function(){

    let text = new fabric.Text("Year",{

        left:260,
        top:240,
        fontSize:28,
        fill:"black",
        fontFamily:"Arial",
        name:"year"

    });

    canvas.add(text);

    canvas.setActiveObject(text);

    setStatus("Year Field Added");

};

// ======================================
// Delete Selected Object
// ======================================

document
.getElementById("deleteObject")
.onclick = function(){

    let obj = canvas.getActiveObject();

    if(obj){

        canvas.remove(obj);

        setStatus("Object Deleted");

    }
    else{

        alert("Please select an object first.");

    }

};