<?php

//возможно ничего не будеть понятно, есть уже до этой задачи созданные классы который помогають мне с парсингом 
function search($plugin_settings)
{
	global $parser;

	$data = $parser->do_request("GET", "https://natural-sciences.ru/ru/article/view?id=34863");
	$res = phpQuery::newDocument($data['body']);

	foreach($res->find('table#table-7 tr') as $tr){
		$tr = pq($tr);
		for($i = 1; $i < 9; $i++){
			$tmp = [
				"name" => $res->find('tr:eq(0) td:eq($i)')->text(),
				"Symptom" => $tr->find('td:eq(0)')->text(),
				"probability" => $tr->find('td:eq($i)')->text(),
			];

			Debugger::getInstance()->info('probability_table ' .print_r($tmp, true));
			EventHooks::after_search_iteration($plugin_settings, $tmp);

		}
	}
	
	foreach($res->find('table#table-8 td') as $tr){
		$tr = pq($tr);
		$tmp = [
			"name" => $tr->find('td:eq(1)')->text(),
			"qty" => $tr->find('td:eq(2)')->text(),
		];
		
		Debugger::getInstance()->info('qty_table ' .print_r($tmp, true));
		EventHooks::after_search_iteration($plugin_settings, $tmp);
		
	}
	
}


?>