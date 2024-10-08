extends Node2D

# Node Characteristic
var id := 0; 

var northNode = null; 
var eastNode = null; 
var southNode = null;
var westNode = null; 

var xCord := 0; 
var yCord := 0;

var nodeValue := -1; 
var nodeSolved = false; 

var visitedCreated = false; 
var visitedSolved = false; 

# Previous Nodes
var previousNodeList = [null, null, null, null]

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass; 
	#$Label.set_text(str(id))

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func visited_neighbors():
	var notVisited = []; 
	if (northNode != null and northNode.visitedCreated == false):
		notVisited.append(1); 
	if (eastNode != null and eastNode.visitedCreated == false): 
		notVisited.append(2); 
	if (southNode != null and southNode.visitedCreated == false):
		notVisited.append(3); 
	if (westNode != null and westNode.visitedCreated == false):
		notVisited.append(4);
		
	return notVisited;  

func get_text():
	return($Label.text)

func upgrade_text(inputText:int):
	$Label.set_text(str(inputText)); 

func _on_area_2d_input_event(viewport: Node, event: InputEvent, shape_idx: int) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		if (nodeValue == 0):
			$Sprite2D.frame = 1;
		else:
			$Sprite2D.frame = 2;
			upgrade_text(nodeValue)
		
func update_previous(inputNode):
	if (previousNodeList[0] == null):
		previousNodeList[0] = inputNode
	elif (previousNodeList[1] == null):
		previousNodeList[1] = inputNode; 
	elif (previousNodeList[2] == null):
		previousNodeList[2] = inputNode; 
	elif (previousNodeList[3] == null):
		previousNodeList[3] = inputNode; 
	else:
		return -1; 
	
func update_visual(spriteValue : int) -> void:
	if (spriteValue >= 4):
		spriteValue = 1; 
	nodeValue = spriteValue

	if (nodeValue == 0):
		$Sprite2D.frame = 1; 
	
func set_value(inputValue :int) -> void:
	if (inputValue >= 4):
		inputValue = 1; 
	nodeValue = inputValue
	
