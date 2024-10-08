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


func _on_area_2d_input_event(viewport: Node, event: InputEvent, shape_idx: int) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		if ($AnimatedSprite2D.frame == 5):
			$'../Game'.restart_game()
			
