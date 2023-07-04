// ----- custom js ----- //

// hide initial
$("#searching").hide();
$("#results-table").hide();
$("#error").hide();

// 全局变量
var url = 'dataset/';
var data = [];

$(function () {

  // sanity check
  console.log("ready!");

  // 获取上传图片按钮
  var uploadBtn = document.querySelector('button');

  // 添加点击事件监听器
  uploadBtn.addEventListener('click', function () {
    // 创建input元素
    var input = document.createElement('input');
    input.type = 'file';

    // 添加change事件监听器
    input.addEventListener('change', function () {
      // 获取上传的图片文件
      var file = input.files[0];
      console.log(file);

      // 创建FormData对象
      var formData = new FormData();
      formData.append('image', file);

      // empty/hide results
      $("#results").empty();
      $("#results-table").hide();
      $("#error").hide();

      // show searching
      $("#searching").show();
      console.log("searching...");

      $.ajax({
        type: "POST",
        url: "/upload",
        data: formData,
        processData: false,
        contentType: false,
        success: function (result) {
          // 获取显示用户上传的图像的img元素
          var uploadedImage = document.getElementById('uploaded-image');
          // 获取用户上传的图像的路径
          var imagePath = result['image_path'];
          // 使用url_for函数来生成静态文件的URL
          var imageUrl = imagePath;
          // 设置img元素的为用户上传的图像
          uploadedImage.src = imageUrl;
          console.log(imageUrl);
          // 设置img元素样式
          uploadedImage.style.height = '300px'
          uploadedImage.style.border = '1px solid #ccc';
          uploadedImage.style.borderRadius = '5px';
          uploadedImage.style.boxShadow = '2px 2px 5px rgba(0, 0, 0, 0.3)';
          uploadedImage.style.padding = '10px';
        },
        error: function (error) {
          console.log(error);
        }
      })

      // 发送POST请求
      $.ajax({
        type: "POST",
        url: "/search",
        data: formData,
        processData: false,
        contentType: false,
        success: function (result) {
          console.log(result.results);
          var data = result.results
          $("#searching").hide();
          // show result table
          $("#results-table").show();
          // 将查询结果添加到dom
          for (i = 0; i < data.length; i++) {
            $("#results").append('<tr><th><a href="' + url + data[i]["image"] + '"><img src="' + url + data[i]["image"] +
              '" class="result-img"></a></th><th>' + data[i]['score'] + '</th></tr>')
          };
        },
        error: function (error) { 
          $("#searching").hide();
          console.log(error);
          // 将错误信息添加到dom
          $("#error").append();
          $("#error").show();
        }
      });
    });

    // 触发input元素的点击事件
    input.click();
  });

});