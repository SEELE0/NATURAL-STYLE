$(function(){
    $("#image1").click(function(){
$("#uploadfile1").click();
})
$("#uploadfile1").change(function(){

    var files=$(this)[0].files[0];    //获取文件信息
    if(files)
    {
        var reader=new FileReader();  //调用FileReader
        reader.onload=function(evt){   //读取操作完成时触发。
            $("#image1").attr('src',evt.target.result)  //将img标签的src绑定为DataURL
        }
    reader.readAsDataURL(files); //将文件读取为 DataURL(base64)
    }
    else{
        alert("上传失败");
    }
})
$("#image2").click(function(){
    $("#uploadfile2").click();
    })
$("#uploadfile2").change(function(){

    var files=$(this)[0].files[0];    //获取文件信息
    if(files)
    {
        var reader=new FileReader();  //调用FileReader
        reader.onload=function(evt){   //读取操作完成时触发。
            $("#image2").attr('src',evt.target.result)  //将img标签的src绑定为DataURL
        }
    reader.readAsDataURL(files); //将文件读取为 DataURL(base64)
    }
    else{
        alert("上传失败");
    }
})
})