<?php
$data = $_POST;

$DBIP     = "localhost";          // 此处填写数据库ip地址
$DBNAME   = $data['dbname'];              // 此处填写数据库名
$DBUSER   = $data['dbuser'];              // 此处填写数据库用户，可以填写root用户
$DBPASSWD = $data['dbpasswd'];             // 此处填写数据库密码
$searchLink = mysqli_connect($DBIP,$DBUSER,$DBPASSWD,$DBNAME) or die("数据库链接失败");
mysqli_set_charset($searchLink,"utf8");

$url=$data['tjurl']."/api.php?app_key=".$data['key']."&method=dsc.goods.insert.post&format=json";
$postData=array(
'cat_id' => $data['cat'],  // 分类ID
'user_id' => '0',   // 用户ID
'goods_name' => $data['title'],  // 商品名
'brand_id' => '0',  // 品牌id
'goods_number' => rand(5,125),  //  商品库存数量
'market_price' => $data['price']*1.2,  // 原价
'shop_price' => $data['price'],   // 现价
'review_status' => '3', // 商品审核状态 3 已审核通过
// 'goods_desc' => $data['detile'],   // 商品描述
'goods_desc' => "1111",   // 商品描述
'original_img'=>$data['hoverimg'],   // 商品原图
'goods_thumb'=>$data['hoverimg'],    // 商品缩略图
'tid' =>'2',    // 运费模板
'goods_sn'=> $data['pre'].rand(10000000,99999999),
'goods_weight'=>'111'   // 商品重量 克
);

$goods_sn = $postData['goods_sn'];//  货号，根据货号修改相关商品数据
$postData = json_encode($postData); // 对变量进行 JSON 编码
$argument=array(
'data' => $postData,
);
$res = curlPost($url,$argument);
// var_dump($res);
$res = (array)json_decode($res,true);
// var_dump($res);
$updateDetileSql = 'update dsc_goods set goods_desc=\''.$data['detile'].'\' where goods_sn="'.$goods_sn.'";';
// echo $updateDetileSql."<br />";
$updateDetileResult = mysqli_query($searchLink,$updateDetileSql);
// var_dump($updateDetileResult);
if ($res['error']==0 && $updateDetileResult) {
	echo "success";
}
else{
	echo "error";
}
function curlPost($url,$res){
	$curl = curl_init(); // 启动一个CURL会话
	curl_setopt($curl, CURLOPT_URL, $url); // 要访问的地址
	curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, 0); // 对认证证书来源的检查
	curl_setopt($curl, CURLOPT_FOLLOWLOCATION, 1); // 使用自动跳转
	curl_setopt($curl, CURLOPT_AUTOREFERER, 1); // 自动设置Referer
	curl_setopt($curl, CURLOPT_POST, 1); // 发送一个常规的Post请求
	curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($res));
	curl_setopt($curl, CURLOPT_TIMEOUT, 30); // 设置超时限制防止死循环
	curl_setopt($curl, CURLOPT_HEADER, 0); // 显示返回的Header区域内容
	curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1); // 获取的信息以文件流的形式返回

	$result = curl_exec($curl); // 执行赋值操作
	curl_close($curl); // 关闭CURL会话
    //这里解析
    return $result;
}