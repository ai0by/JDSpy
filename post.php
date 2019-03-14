<?php
$data = $_POST;

$DBIP     = "localhost";
$DBNAME   = $data['dbname'];
$DBUSER   = $data['dbuser'];
$DBPASSWD = $data['dbpasswd'];
$searchLink = mysqli_connect($DBIP,$DBUSER,$DBPASSWD,$DBNAME) or die("数据库链接失败");
mysqli_set_charset($searchLink,"utf8");

$insertUrl=$data['tjurl']."/api.php?app_key=".$data['key']."&method=dsc.goods.insert.post&format=json";
$updateGrallyUrl = $data['tjurl']."/api.php?app_key=".$data['key']."&method=dsc.goods.gallery.insert.post&format=json";
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

$imglist = $data['imglist'];
$imglist = explode(",", $imglist);

$goods_sn = $postData['goods_sn'];//  货号，根据货号修改相关商品数据
$postData = json_encode($postData); // 对变量进行 JSON 编码
$argument=array(
'data' => $postData,
);
$res = curlPost($insertUrl,$argument);
$res = (array)json_decode($res,true);
$updateDetileSql = 'update dsc_goods set goods_desc=\''.$data['detile'].'\' where goods_sn="'.$goods_sn.'";';
$updateDetileResult = mysqli_query($searchLink,$updateDetileSql);
$searchGoodsSql = 'select * from dsc_goods where goods_sn="'.$goods_sn.'";';
$searchGoodsResult = mysqli_query($searchLink,$searchGoodsSql);
$goods_id = mysqli_fetch_array($searchGoodsResult);
$goods_id = $goods_id['goods_id'];

for ($i=0; $i < count($imglist)-1; $i++) {
	$grallyData=array(
	'goods_id' => (int)$goods_id,
	'img_url' => $imglist[$i],
	'img_desc' => $i,
	'thumb_url' => str_replace("800x800","400x400",$imglist[$i]),
	'img_original' => $imglist[$i],
	);
	$grallyData = json_encode($grallyData);
	$grallyData=array(
	'data' => $grallyData
	);
	$grallyRes = curlPost($updateGrallyUrl,$grallyData);
	// $grallyRes = (array)json_decode($res,true);
}

if ($res['error']==0 && $updateDetileResult) {
	echo "success";
}
else{
	echo "error";
}


function curlPost($url,$res){
	$curl = curl_init();
	curl_setopt($curl, CURLOPT_URL, $url);
	curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, 0);
	curl_setopt($curl, CURLOPT_FOLLOWLOCATION, 1);
	curl_setopt($curl, CURLOPT_AUTOREFERER, 1);
	curl_setopt($curl, CURLOPT_POST, 1);
	curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($res));
	curl_setopt($curl, CURLOPT_TIMEOUT, 30);
	curl_setopt($curl, CURLOPT_HEADER, 0);
	curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);

	$result = curl_exec($curl);
	curl_close($curl);
    return $result;
}