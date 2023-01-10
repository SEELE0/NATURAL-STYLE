$(function(){
    $("#image").click(function(){
$("#uploadfile").click();
})
$("#uploadfile").change(function(){

    var files=$(this)[0].files[0];    //获取文件信息
    if(files)
    {
        var reader=new FileReader();  //调用FileReader
        reader.onload=function(evt){   //读取操作完成时触发。
            $("#image").attr('src',evt.target.result)  //将img标签的src绑定为DataURL
        }
    reader.readAsDataURL(files); //将文件读取为 DataURL(base64)
    }
    else{
        alert("上传失败");
    }
})
})