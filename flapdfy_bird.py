PDF_TEMPLATE = """
%PDF-1.6

1 0 obj
<<
  /AcroForm <<
    /Fields [ ###FIELD_LIST### ]
  >>
  /Pages <<
    /Count 1
    /Kids [ 16 0 R ]
    /Type /Pages
  >>
  /OpenAction 17 0 R
  /Type /Catalog
>>
endobj

21 0 obj
[ ###FIELD_LIST### ]
endobj

###FIELDS###

16 0 obj
<<
  /Annots 21 0 R
  /Contents << >>
  /CropBox [ 0.0 0.0 612.0 792.0 ]
  /MediaBox [ 0.0 0.0 612.0 792.0 ]
  /Parent 7 0 R
  /Resources << >>
  /Rotate 0
  /Type /Page
>>
endobj

17 0 obj
<<
  /JS 42 0 R
  /S /JavaScript
>>
endobj

42 0 obj
<< >>
stream
// Game constants
var GAME_WIDTH = 400;
var GAME_HEIGHT = 600;
var BIRD_SIZE = 20;
var BIRD_X = 50;
var PIPE_WIDTH = 50;
var PIPE_GAP = 150;
var GRAVITY = 0.5;
var JUMP_FORCE = 8;
var PIPE_SPEED = 2;
var TICK_INTERVAL = 16;

// Game state
var bird_y = GAME_HEIGHT/2;
var bird_velocity = 0;
var pipes = [];
var score = 0;
var game_over = false;
var interval = null;
var isGameRunning = false;

// Utility function for setInterval
function setInterval(cb, ms) {
    evalStr = "(" + cb.toString() + ")();";
    return app.setInterval(evalStr, ms);
}

// Game initialization
function init_game() {
    if (isGameRunning) return;
    
    // Reset game state
    bird_y = GAME_HEIGHT/2;
    bird_velocity = 0;
    pipes = [];
    score = 0;
    game_over = false;
    isGameRunning = true;
    
    // Create initial pipes
    spawn_pipe();
    
    // Start game loop
    interval = setInterval(game_loop, TICK_INTERVAL);
    
    // Hide start button
    this.getField("start_btn").hidden = true;
    
    // Show flap button
    this.getField("flap_btn").hidden = false;
    
    // Update score display
    this.getField("score_text").value = "Score: 0";
    
    // Initial draw
    draw();
}

function spawn_pipe() {
    var gap_y = Math.floor(Math.random() * (GAME_HEIGHT - PIPE_GAP - 100) + 50);
    pipes.push({
        x: GAME_WIDTH,
        gap_y: gap_y,
        passed: false
    });
}

function handle_input() {
    if (!game_over && isGameRunning) {
        bird_velocity = JUMP_FORCE;
    }
}

function update() {
    if (game_over || !isGameRunning) return;
    
    // Update bird (reversed gravity direction)
    bird_velocity -= GRAVITY;
    bird_y += bird_velocity;
    
    // Check collisions
    if (bird_y < 0 || bird_y > GAME_HEIGHT) {
        end_game();
        return;
    }
    
    // Update pipes
    for (var i = pipes.length-1; i >= 0; i--) {
        var pipe = pipes[i];
        pipe.x -= PIPE_SPEED;
        
        // Improved collision detection
        if (pipe.x < (BIRD_X + BIRD_SIZE) && (pipe.x + PIPE_WIDTH) > BIRD_X) {
            // Convert bird_y to center point
            var bird_center = bird_y + (BIRD_SIZE/2);
            if (bird_center < (pipe.gap_y + BIRD_SIZE/2) || 
                bird_center > (pipe.gap_y + PIPE_GAP - BIRD_SIZE/2)) {
                end_game();
                return;
            }
        }
        
        // Score points (adjusted for new bird position)
        if (!pipe.passed && pipe.x + PIPE_WIDTH < BIRD_X) {
            pipe.passed = true;
            score++;
            this.getField("score_text").value = "Score: " + score;
        }
        
        // Remove old pipes
        if (pipe.x < -PIPE_WIDTH) {
            pipes.splice(i, 1);
        }
    }
    
    // Spawn new pipes
    if (pipes.length == 0 || pipes[pipes.length-1].x < GAME_WIDTH - 300) {
        spawn_pipe();
    }
}

function draw() {
    try {
        // Clear screen
        for (var x = 0; x < GAME_WIDTH/10; x++) {
            for (var y = 0; y < GAME_HEIGHT/10; y++) {
                var field = this.getField("p_"+x+"_"+y);
                if (field) {
                    field.hidden = true;
                }
            }
        }
        
        if (!isGameRunning) return;
        
        // Draw bird (using BIRD_X constant)
        var bird_x = Math.floor(BIRD_X/10);
        var bird_y_grid = Math.floor(bird_y/10);
        var birdField = this.getField("p_"+bird_x+"_"+bird_y_grid);
        if (birdField) {
            birdField.hidden = false;
        }
        
        // Draw pipes
        for (var pipe of pipes) {
            var pipe_x = Math.floor(pipe.x/10);
            for (var y = 0; y < GAME_HEIGHT/10; y++) {
                if (y*10 < pipe.gap_y || y*10 > pipe.gap_y + PIPE_GAP) {
                    var pipeField = this.getField("p_"+pipe_x+"_"+y);
                    if (pipeField) {
                        pipeField.hidden = false;
                    }
                }
            }
        }
    } catch (e) {
        app.alert("Draw error: " + e.toString());
    }
}

function game_loop() {
    try {
        update();
        draw();
    } catch (e) {
        app.alert("Game loop error: " + e.toString());
    }
}

function end_game() {
    game_over = true;
    isGameRunning = false;
    if (interval !== null) {
        app.clearInterval(interval);
        interval = null;
    }
    app.alert("Game Over! Score: " + score);
    this.getField("start_btn").hidden = false;
    this.getField("flap_btn").hidden = true;
}

// Setup initial state
function setup() {
    try {
        // Make start button clickable
        var startBtn = this.getField("start_btn");
        if (startBtn) {
            startBtn.setAction("MouseDown", "init_game();");
        }
        
        // Make flap button clickable
        var flapBtn = this.getField("flap_btn");
        if (flapBtn) {
            flapBtn.setAction("MouseDown", "handle_input();");
        }
        
        // Hide flap button initially
        this.getField("flap_btn").hidden = true;
        
        // Initial draw
        draw();
    } catch (e) {
        app.alert("Setup error: " + e.toString());
    }
}

// Call setup when PDF loads
setup();

endstream
endobj

trailer
<<
  /Root 1 0 R
>>
%%EOF
"""

PIXEL_OBJ = """
###IDX### 0 obj
<<
  /FT /Btn
  /Ff 65536
  /MK <<
    /BG [ 0 0.5 0.8 ]
    /BC [ 0 0 0 ]
  >>
  /Border [ 0 0 1 ]
  /P 16 0 R
  /Rect [ ###RECT### ]
  /Subtype /Widget
  /T (p_###X###_###Y###)
  /Type /Annot
>>
endobj
"""

BUTTON_OBJ = """
###IDX### 0 obj
<<
  /FT /Btn
  /Ff 65536
  /MK <<
    /BG [ 0.8 0.8 0.8 ]
    /CA (###LABEL###)
  >>
  /P 16 0 R
  /Rect [ ###RECT### ]
  /Subtype /Widget
  /T (###NAME###)
  /Type /Annot
  /A <<
    /S /JavaScript
    /JS (try { ###ACTION### } catch(e) { app.alert(e.toString()); })
  >>
>>
endobj
"""

TEXT_OBJ = """
###IDX### 0 obj
<<
  /FT /Tx
  /Ff 1
  /P 16 0 R
  /Rect [ ###RECT### ]
  /Subtype /Widget
  /T (###NAME###)
  /V (###VALUE###)
  /Type /Annot
>>
endobj
"""

def generate_flappy_bird_pdf():
    fields = []
    field_indexes = []
    obj_idx = 50
    
    # Game area dimensions
    GRID_WIDTH = 40  # 400/10
    GRID_HEIGHT = 60 # 600/10
    GRID_OFF_X = 100
    GRID_OFF_Y = 100
    PIXEL_SIZE = 10
    
    # Generate pixel grid
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pixel = PIXEL_OBJ.replace("###IDX###", str(obj_idx))
            pixel = pixel.replace("###X###", str(x))
            pixel = pixel.replace("###Y###", str(y))
            rect = f"{GRID_OFF_X + x*PIXEL_SIZE} {GRID_OFF_Y + y*PIXEL_SIZE} {GRID_OFF_X + (x+1)*PIXEL_SIZE} {GRID_OFF_Y + (y+1)*PIXEL_SIZE}"
            pixel = pixel.replace("###RECT###", rect)
            
            fields.append(pixel)
            field_indexes.append(obj_idx)
            obj_idx += 1
    
    # Add start button
    button = BUTTON_OBJ.replace("###IDX###", str(obj_idx))
    button = button.replace("###LABEL###", "Start Game")
    button = button.replace("###NAME###", "start_btn")
    button = button.replace("###ACTION###", "init_game();")
    button = button.replace("###RECT###", f"{GRID_OFF_X + 150} {GRID_OFF_Y + 250} {GRID_OFF_X + 250} {GRID_OFF_Y + 300}")
    fields.append(button)
    field_indexes.append(obj_idx)
    obj_idx += 1
    
    # Add flap button
    button = BUTTON_OBJ.replace("###IDX###", str(obj_idx))
    button = button.replace("###LABEL###", "FLAP!")
    button = button.replace("###NAME###", "flap_btn")
    button = button.replace("###ACTION###", "handle_input();")
    button = button.replace("###RECT###", f"{GRID_OFF_X + 150} {GRID_OFF_Y - 50} {GRID_OFF_X + 250} {GRID_OFF_Y - 20}")
    fields.append(button)
    field_indexes.append(obj_idx)
    obj_idx += 1
    
    # Add score text
    text = TEXT_OBJ.replace("###IDX###", str(obj_idx))
    text = text.replace("###NAME###", "score_text")
    text = text.replace("###VALUE###", "Score: 0")
    text = text.replace("###RECT###", f"{GRID_OFF_X + 150} {GRID_OFF_Y + GRID_HEIGHT*PIXEL_SIZE + 20} {GRID_OFF_X + 250} {GRID_OFF_Y + GRID_HEIGHT*PIXEL_SIZE + 40}")
    fields.append(text)
    field_indexes.append(obj_idx)
    obj_idx += 1
    
    # Generate PDF
    pdf_content = PDF_TEMPLATE.replace("###FIELDS###", "\n".join(fields))
    pdf_content = pdf_content.replace("###FIELD_LIST###", " ".join([f"{i} 0 R" for i in field_indexes]))
    
    with open("flappy_bird.pdf", "w") as f:
        f.write(pdf_content)

if __name__ == "__main__":
    generate_flappy_bird_pdf()