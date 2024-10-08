extends Node2D

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass;

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func update_visual(selectedFrame: int) -> void:
	$AnimatedSprite2D.frame = selectedFrame; 

func update_info(sumInput : int, countInput: int) -> void:
	$SumDisplay.set_text(str(sumInput)); 
	$voltCount.set_text(str(countInput));
