const fileInput=document.getElementById("csvFile");
const fileName=document.getElementById("filename");
const button=document.getElementById("uploadBtn");
const loader=document.getElementById("loader");
const status=document.getElementById("status");

fileInput.addEventListener("change",()=>{
    if(fileInput.files.length){
        fileName.innerHTML=fileInput.files[0].name;
    }
});
button.onclick=async()=>{
    if(fileInput.files.length===0){
        alert("Select a CSV file");
        return;
    }
    const formData=new FormData();
    formData.append("file",fileInput.files[0]);
    loader.style.display="block";
    status.innerHTML="Analyzing logs...";
    button.disabled=true;
    try{
        const response=await fetch("/classify/",{
            method:"POST",
            body:formData
        });
        if(!response.ok){
            throw new Error("Classification failed");
        }
        const blob=await response.blob();
        const url=window.URL.createObjectURL(blob);
        const a=document.createElement("a");
        a.href=url;
        a.download="output.csv";
        a.click();
        loader.style.display="none";
        status.innerHTML="✅ Classification completed successfully.";
    }
    catch(err){
        loader.style.display="none";
        status.innerHTML="❌ "+err.message;
    }
    button.disabled=false;
}