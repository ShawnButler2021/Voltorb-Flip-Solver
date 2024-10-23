extends Node2D

var counter := 0; 
var size := 5; 

var previousNode = null;
var nextNode = null; 
var tailNode = null; 

var rootNode = null; 

var nodeCreationList = []
var sideHintCreationList = []

var columnVoltCount = []
var rowVoltCount = []


@onready var nodeSpawn = preload("res://node.tscn")
@onready var hintSpawn = preload("res://sideHints.tscn")

func test_cases(id = 0) -> void:
	if (id == 0):
		columnVoltCount = [2, 2, 2, 1, 1]
		rowVoltCount = [2, 1, 1, 2, 2]
	elif (id == 1):
		columnVoltCount = [1, 1, 1, 2, 2]
		rowVoltCount = [0, 2, 2, 0, 3]

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass; 

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass; 

func _input(event: InputEvent) -> void: 	
	if event is InputEventKey and event.is_pressed():
		if event.keycode == KEY_C:
			clear_variables()
			make_grid(size); 
			
			var inputNode = find_node(nodeCreationList, 0, 0);
			rootNode = find_node(nodeCreationList, 0, 0)
			#solve_Voltflip(size, rootNode, rootNode)
			
			#make_sideHint(size);
			
			#print(get_row_VoltCount(size))
			#print(get_column_VoltCount(size))
			#print(""); 
			#print(get_column_sum(size))
			#print(get_row_sum(size))
			
			set_sideHint(
				[2, 1, 5, 5, 12],
				[2, 1, 9, 6, 4],
				[3, 4, 2, 3, 1],
				[3, 1, 3, 3, 3],
			)
			
			#connect_nodes(inputNode, null); 

func clear_variables():
	counter = 0; 
	
	for i in nodeCreationList:
		i.queue_free()
	for i in sideHintCreationList:
		i.queue_free()
	nodeCreationList = []
	sideHintCreationList = []
	rootNode = null; 
	previousNode = null; 

func find_node(inputList, desiredX, desiredY):
	for eachNode in inputList: 
		if eachNode.xCord == desiredX and eachNode.yCord == desiredY:
			return eachNode; 

func make_grid(size: int) -> void:
	for i in size:
		for j in size: 
			var b = nodeSpawn.instantiate()
			counter += 1
			b.id = counter; 
			b.xCord = i; 
			b.yCord = j; 
			b.global_position = Vector2(i * 60, j * 60); 
			# Create Voltblip value
			b.set_value(randi_range(0, 5))
			
			if (i == j) and (j == 3):
				$Camera2D.global_position = b.global_position; 
			
			nodeCreationList.append(b)
			get_parent().add_child(b)
		#	
	var copyList = nodeCreationList.duplicate()
		
	for i in size:
		for j in size:
			var b = copyList.pop_front()
			if (b.xCord < size):
				b.eastNode = find_node(nodeCreationList, b.xCord + 1, b.yCord);
			if (b.yCord < size):
				b.southNode = find_node(nodeCreationList, b.xCord, b.yCord + 1);	
			if (b.xCord > 0):
				b.westNode = find_node(nodeCreationList, b.xCord - 1, b.yCord);	
			if (b.yCord > 0):
				b.northNode = find_node(nodeCreationList,b.xCord, b.yCord - 1);	

func make_sideHint(size: int) -> void:
	
	var sumColumnnList = get_column_sum(size)
	var sumRowList = get_row_sum(size)
	
	var countColumnList = get_column_VoltCount(size)
	var countRowList = get_row_VoltCount(size)
	
	# Rows Hints
	for i in size:
		var b = hintSpawn.instantiate()
		b.global_position = Vector2((size) * 60,  i * 60); 
		b.update_info(sumRowList[i], countRowList[i])
		b.update_visual(i)
		sideHintCreationList.append(b)
		get_parent().add_child(b)
		
	for i in size:
		var b = hintSpawn.instantiate()
		b.global_position = Vector2(i * 60,  size * 60); 
		b.update_visual(i)
		b.update_info(sumColumnnList[i], countColumnList[i])
		sideHintCreationList.append(b)
		get_parent().add_child(b)

	var b = hintSpawn.instantiate()
	b.global_position = Vector2(size * 60,  size * 60);
	b.update_visual(size)
	sideHintCreationList.append(b)
	get_parent().add_child(b) 

func get_column_sum(size: int) -> Array:
	var selectedNode = rootNode; 
	var selectedColumn = rootNode; 
	var columnSums = []
	for i in size: 
		var sum = 0; 
		for j in size: 
			sum = sum + selectedNode.nodeValue
			selectedNode = selectedNode.southNode
			 
		columnSums.append(sum)
		selectedColumn = selectedColumn.eastNode
		selectedNode = selectedColumn
		
	return(columnSums)

func get_row_sum(size:int) -> Array:
	var selectedNode = rootNode; 
	var selectedRow = rootNode; 
	var rowSums = []
	for i in size: 
		var sum = 0; 
		for j in size: 
			sum = sum + selectedNode.nodeValue
			selectedNode = selectedNode.eastNode
			 
		rowSums.append(sum)
		selectedRow = selectedRow.southNode
		selectedNode = selectedRow
		
	return(rowSums)

func get_voltflip_nodes(size:int) -> Array:
	var voltflipNodes = []
	for i in nodeCreationList:
		if (i.nodeValue == 0):
			voltflipNodes.append(i)

	return(voltflipNodes)

func get_row_VoltCount(size:int) -> Array:
	var selectedNode = rootNode; 
	var selectedRow = rootNode; 
	var rowCount = []
	for i in size: 
		var count = 0; 
		for j in size: 
			if selectedNode.nodeValue == 0:
				count += 1; 
			selectedNode = selectedNode.eastNode
			 
		rowCount.append(count)
		selectedRow = selectedRow.southNode
		selectedNode = selectedRow
		
	return(rowCount)

func get_column_VoltCount(size:int) -> Array:
	var selectedNode = rootNode; 
	var selectedColumn = rootNode; 
	var columnCount = []
	for i in size: 
		var count = 0; 
		for j in size: 
			if selectedNode.nodeValue == 0:
				count += 1; 
			selectedNode = selectedNode.southNode
			 
		columnCount.append(count)
		selectedColumn = selectedColumn.eastNode
		selectedNode = selectedColumn
		
	return(columnCount)

#Not being used. 
func solve_Voltflip(size:int, selectedNode:Node, selectedRow:Node) -> bool:
	print("SelectedNode: ", selectedNode.xCord, "  ", selectedNode.yCord)
	print("Info: ", get_row_VoltCount(size)[selectedNode.yCord] , "  ",  rowVoltCount[selectedNode.yCord])
	if (get_row_VoltCount(size)[selectedNode.yCord] < rowVoltCount[selectedNode.yCord]) and (get_column_VoltCount(size)[selectedNode.xCord] < columnVoltCount[selectedNode.xCord]):
		selectedNode.update_visual(0)
	else:
		selectedNode.update_visual(-1)
		
	if (get_row_VoltCount(size)[selectedNode.yCord] == rowVoltCount[selectedNode.yCord]):
		if (selectedRow.southNode != null):
			print("a: ", selectedNode.xCord, "  ", selectedNode.yCord)
			selectedNode = selectedRow.southNode; 
			selectedRow = selectedNode
		else:
			return(true)
	else:
		if (selectedNode.eastNode != null):
			selectedNode = selectedNode.eastNode; 
			print("b: ", selectedNode.xCord, "  ", selectedNode.yCord)
		else:
			if (selectedRow.southNode != null):
				selectedNode = selectedRow.southNode; 
				selectedRow = selectedNode
				print("c: ", selectedNode.xCord, "  ", selectedNode.yCord)
			else:
				return(true)
	
	if (get_row_VoltCount(size) == rowVoltCount) and (get_column_sum(size) == columnVoltCount):
		return(true)
	else:
		return(solve_Voltflip(size, selectedNode, selectedRow))	
		
func connect_nodes(inputNode, inputPrevious):
	var notVisited = inputNode.visited_neighbors(); 

	if (notVisited.size() > 0):
		var selectedDirection = randi_range(0, notVisited.size() - 1)
		selectedDirection = notVisited[selectedDirection]
		var connectingNode = null; 
		
		if (selectedDirection == 1):
			connectingNode = inputNode.northNode; 
		if (selectedDirection == 2):
			connectingNode = inputNode.eastNode; 
		if (selectedDirection == 3):
			connectingNode = inputNode.southNode; 
		if (selectedDirection == 4):
			connectingNode = inputNode.westNode; 
			
		connectingNode.update_previous(inputNode)
		
		if (inputNode.visitedCreated == false):
			counter += 1; 
			inputNode.upgrade_text(counter); 
			inputNode.visitedCreated = true; 
			
		connect_nodes(connectingNode, inputNode)
	else:
		if (inputNode.visitedCreated == false):
			counter += 1; 
			inputNode.visitedCreated = true; 
			inputNode.upgrade_text(counter); 
			inputNode.update_previous(inputPrevious); 
		
		if (inputNode.id == 1):
			return true; 
		else:
			#connect_nodes(inputNode.previousNode, inputNode.previousNode.previousNode); 
			pass; 
			
func _on_timer_timeout() -> void:
	restart_game()

func restart_game() -> void:
	clear_variables()
	make_grid(size); 
		
	var inputNode = find_node(nodeCreationList, 0, 0);
	rootNode = find_node(nodeCreationList, 0, 0)
	#solve_Voltflip(size, rootNode, rootNode)
		
	#make_sideHint(size);
	
	set_sideHint(
	[2, 1, 5, 5, 12],
	[2, 1, 9, 6, 4],
	[3, 4, 2, 3, 1],
	[3, 1, 3, 3, 3],
	)

func set_sideHint(rowVoltCounts:Array, colVoltCounts:Array, rowCoinCount:Array, colCoinCounts:Array) -> void: 
	for i in sideHintCreationList:
		i.queue_free()
	sideHintCreationList = []
	
	for i in size:
		var b = hintSpawn.instantiate()
		b.global_position = Vector2((size) * 60,  i * 60); 
		b.update_info(rowVoltCounts[i], rowCoinCount[i])
		b.update_visual(i)
		sideHintCreationList.append(b)
		get_parent().add_child(b)
		
	for i in size:
		var b = hintSpawn.instantiate()
		b.global_position = Vector2(i * 60,  size * 60); 
		b.update_visual(i)
		b.update_info(colVoltCounts[i], colCoinCounts[i])
		sideHintCreationList.append(b)
		get_parent().add_child(b)
		
