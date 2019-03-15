<?php
// 将本文件放置在ECShop根目录下
$data = $_POST;

$DBIP     = "localhost";         
$DBNAME   = $data['dbname'];              
$DBUSER   = $data['dbuser'];             
$DBPASSWD = $data['dbpasswd'];             
$searchLink = mysqli_connect($DBIP,$DBUSER,$DBPASSWD,$DBNAME) or die("数据库链接失败");
mysqli_set_charset($searchLink,"utf8");

$postData=array(
'cat_id' => $data['cat'],  // 分类ID
'goods_name' => $data['title'],  // 商品名
'goods_number' => rand(5,125),  //  商品库存数量
'market_price' => $data['price']*1.2,  // 原价
'shop_price' => $data['price'],   // 现价
'goods_desc' => $data['detile'],   // 商品描述
// 'goods_desc' => "1111",   // 商品描述
'original_img'=>$data['hoverimg'],   // 商品原图
'goods_thumb'=>$data['hoverimg'],    // 商品缩略图
'goods_img'=>$data['hoverimg'],
'goods_sn'=> $data['pre'].rand(10000000,99999999),
);

$goods_sn = $postData['goods_sn'];//  货号，根据货号修改相关商品数据

$insertSql = 'insert into ecs_goods (goods_img,cat_id,goods_name,goods_number,market_price,shop_price,goods_desc,original_img,goods_thumb,goods_sn)VALUES ("'.$postData['goods_img'].'","'.$postData['cat_id'].'","'.$postData['goods_name'].'","'.$postData['goods_number'].'","'.$postData['market_price'].'","'.$postData['shop_price'].'",\''.$postData['goods_desc'].'\',"'.$postData['original_img'].'","'.$postData['goods_thumb'].'","'.$postData['goods_sn'].'")';

// echo $insertSql;
$insertResult = mysqli_query($searchLink,$insertSql);

$searchGoodsSql = 'select * from ecs_goods where goods_sn="'.$goods_sn.'";';
$searchGoodsResult = mysqli_query($searchLink,$searchGoodsSql);
$goods_id = mysqli_fetch_array($searchGoodsResult);
$goods_id = $goods_id['goods_id'];

$imglist = $data['imglist'];
$imglist = explode(",", $imglist);
for ($i=0; $i < count($imglist)-1; $i++) { 
	$grallyData=array(
	'goods_id' => (int)$goods_id,
	'img_url' => $imglist[$i],
	'img_desc' => $i,
	'thumb_url' => str_replace("800x800","400x400",$imglist[$i]),
	'img_original' => $imglist[$i],
	);
	$insertGrallySql = 'insert into ecs_goods_gallery (goods_id,img_url,img_desc,thumb_url,img_original) VALUES ("'.$grallyData['goods_id'].'","'.$grallyData['img_url'].'","'.$grallyData['img_desc'].'","'.$grallyData['thumb_url'].'","'.$grallyData['img_original'].'")';
	mysqli_query($searchLink,$insertGrallySql);
	// echo $insertGrallySql;
}

if ($insertResult) {
	echo "success";
}else{
	echo "error";
}
