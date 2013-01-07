
window.onload = windowReady;

function drawCurved(context, x1, y1, x2, y2, direction1, direction2, lineWidth, scale)
{
    var centerX;
    var centerY;
    var startingAngle;
    var endingAngle;
    var counterclockwise = false;
    // Value fixed by vario-system:
    var radius = 205;
    console.log(x1 + " " + y1);
    console.log(x2 + " " + y2);
    if (direction1 == 0)
    {
        if (direction2 == 5 )
        {
            centerY = y1;
            centerX = x1 - radius;
            startingAngle = 0;
            endingAngle = 0.25 * Math.PI;
        }
        else
        // direction == 3
        {
            counterclockwise = true;
            centerY = y1;
            centerX = x1 + radius;
            startingAngle = Math.PI;
            endingAngle = 0.75 * Math.PI;
        }
    }

    if (direction1 == 1)
    {
        if (direction2 == 6 )
        {
            centerY = y2 + radius;
            centerX = x2;
            startingAngle = 0.25 * Math.PI;
            endingAngle = 0.5 * Math.PI;
        }
        else
        // direction == 4
        {
            counterclockwise = true;
            centerY = y2;
            centerX = x2 + radius;
            startingAngle = 1.25 * Math.PI;
            endingAngle = Math.PI;
        }
    }

    if (direction1 == 2)
    {
        if (direction2 == 7 )
        {
            centerY = y1 + radius;
            centerX = x1;
            startingAngle = 0.5 * Math.PI;
            endingAngle = 0.75 * Math.PI;
        }
        else
        // direction == 5
        {
            counterclockwise = true;
            centerY = y1 - radius;
            centerX = x1;
            startingAngle = 1.5 * Math.PI;
            endingAngle = 1.25 * Math.PI;
        }
    }

    if (direction1 == 3)
    {
        if (direction2 == 0 )
        {
            centerY = y2;
            centerX = x2 + radius;
            startingAngle = 0.75 * Math.PI;
            endingAngle = Math.PI;
        }
        else
        // direction == 6
        {
            counterclockwise = true;
            centerY = y2 - radius;
            centerX = x2;
            startingAngle = 1.75 * Math.PI;
            endingAngle = 1.5 * Math.PI;
        }
    }

    if (direction1 == 4)
    {
        if (direction2 == 1 )
        {
            centerY = y1;
            centerX = x1 + radius;
            startingAngle = Math.PI;
            endingAngle = 1.25 * Math.PI;
        }
        else
        // direction == 7
        {
            counterclockwise = true;
            centerY = y1;
            centerX = x1 - radius;
            startingAngle = 0;
            endingAngle = 1.75 * Math.PI;
        }
    }

    if (direction1 == 5)
    {
        if (direction2 == 2 )
        {
            centerY = y2 - radius;
            centerX = x2;
            startingAngle = 1.25 * Math.PI;
            endingAngle = 1.5 * Math.PI;
        }
        else
        // direction == 0
        {
            counterclockwise = true;
            centerY = y2;
            centerX = x2 - radius;
            startingAngle = 0.25 * Math.PI;
            endingAngle = 0;
        }
    }

    if (direction1 == 6)
    {
        if (direction2 == 3 )
        {
            centerY = y1 - radius;
            centerX = x1;
            startingAngle = 1.5 * Math.PI;
            endingAngle = 1.75 * Math.PI;
        }
        else
        // direction == 1
        {
            counterclockwise = true;
            centerY = y1 + radius;
            centerX = x1;
            startingAngle = 0.5 * Math.PI;
            endingAngle = 0.25 * Math.PI;
        }
    }

    if (direction1 == 7)
    {
        if (direction2 == 4 )
        {
            centerY = y2;
            centerX = x2 - radius;
            startingAngle = 1.75 * Math.PI;
            endingAngle = 0;
        }
        else
        // direction == 2
        {
            counterclockwise = true;
            centerY = y2 + radius;
            centerX = x2;
            startingAngle = 0.75 * Math.PI;
            endingAngle = 0.5 * Math.PI;
        }
    }


    context.beginPath();
    console.log("Drawing with:" + centerX + "," + convertY(centerY) + "," + radius + "," + startingAngle + "," + endingAngle + "," + counterclockwise)
    context.rotate(0.75*Math.PI)
    context.arc(centerX, convertY(centerY), radius, startingAngle, endingAngle, counterclockwise);

    context.lineWidth = lineWidth;
    context.strokeStyle = 'green';
    context.stroke();

    context.closePath();

}

function convertY(y)
{
//     return 10000 - y;
    return y;
}

function drawSide(context, x, y, direction, _length)
{
    var startX;
    var startY;
    var endX;
    var endY;
    var lineWidth = 2;
    var strokeStyle = 'white';

    if(direction == 0)
    {
        startX = x - _length / 2;
        startY = y;
        endX = x + _length / 2;
        endY = y;
    }
    if(direction == 1)
    {
        startX = x - Math.cos(45) * _length;
        startY = y + Math.cos(45) * _length;
        endX = x + Math.cos(45) * _length;
        endY = y - Math.cos(45) * _length;
    }
    if(direction == 2)
    {
        startX = x;
        startY = y - _length / 2;
        endX = x;
        endY = y + _length / 2;
    }
    if(direction == 3)
    {
        startX = x - Math.cos(45) * _length;
        startY = y - Math.cos(45) * _length;
        endX = x + Math.cos(45) * _length;
        endY = y + Math.cos(45) * _length;
    }
    if(direction == 4)
    {
        startX = x - _length / 2;
        startY = y;
        endX = x + _length / 2;
        endY = y;
    }
    if(direction == 5)
    {
        startX = x - Math.cos(45) * _length;
        startY = y + Math.cos(45) * _length;
        endX = x + Math.cos(45) * _length;
        endY = y - Math.cos(45) * _length;
    }
    if(direction == 6)
    {
        startX = x;
        startY = y - _length / 2;
        endX = x;
        endY = y + _length / 2;
    }
    if(direction == 7)
    {
        startX = x - Math.cos(45) * _length;
        startY = y - Math.cos(45) * _length;
        endX = x + Math.cos(45) * _length;
        endY = y + Math.cos(45) * _length;
    }

    context.beginPath();
    context.moveTo(startX, convertY(startY));
    context.lineTo(endX, convertY(endY));
    context.lineWidth = lineWidth;
    context.strokeStyle = strokeStyle;
    context.stroke();
    context.closePath();

}

function drawCanvasOutline(context, scale)
{
    context.beginPath();
    context.moveTo(0, 0);
    context.lineTo(context.canvas.width, 0);
    context.lineTo(context.canvas.width, context.canvas.height);
    context.lineTo(0, context.canvas.height);
    context.lineTo(0, 0);
    context.lineWidth = 4;
    context.strokeStyle = 'black';
    context.stroke();
    context.closePath();
}

function windowReady()
{



    var lineWidth = 10;
    var max_x = railway["max_x"];
    var max_y = railway["max_y"];
    var min_x = railway["min_x"];
    var min_y = railway["min_y"];
    var shift_x = 20;
    var shift_y = 20;
    var scale = 0.5;
    var context = document.getElementById("canvasId").getContext("2d");
    var width = (max_x - min_x + shift_x);
    var height = (max_y - min_y + shift_y);


    console.log("shift_x " + shift_x);
    console.log("shift_y " + shift_y);
    // console.log(railway)


    context.canvas.height = height;
    context.canvas.width = width;


//     context.translate(shift_x, context.canvas.height + shift_y);   // reset where 0,0 is located
//     context.scale(1,-1); // invert
//     context.translate(0, context.canvas.height);
//     context.scale(scale, -scale);
//     context.translate(shift_x, shift_y);


//     context.canvas.height = 500;
//     context.canvas.width = 500;


    drawCanvasOutline(context, scale);
    context.translate(shift_x/2, height - shift_y/2);
    context.scale(scale, -scale);
//     context.scale(scale, scale);





    console.log("canvas height: " + context.canvas.height);
    console.log("canvas width:" + context.canvas.width);








    for (var rail in railway["rails"]) //Parcourir le dictionnaire.
    {
        // console.log(rail);
        var first_point = new Boolean(true);
        // context.beginPath();
        var curved = railway["rails"][rail]["curved"];
        var reverted = railway["rails"][rail]["reverted"];
        // console.log(curved);
        // console.log(reverted);
        for (var side in railway["rails"][rail]["sides"])
        {
            var direction = railway["rails"][rail]["sides"][side]["direction"];
            // console.log(side);
            // console.log(railway["rails"][rail]["sides"][side]["x"]);
            // console.log(railway["rails"][rail]["sides"][side]["y"]);
            if (curved)
                {
                if (first_point)
                {
                    var first_point_x = railway["rails"][rail]["sides"][side]["x"];
                    var first_point_y = railway["rails"][rail]["sides"][side]["y"];
                    var first_point_direction = railway["rails"][rail]["sides"][side]["direction"];
                    // context.moveTo(railway["rails"][rail]["sides"][side]["x"],railway["rails"][rail]["sides"][side]["y"],3,3);
                    first_point = false;
                }
                else
                {
                    drawCurved(context, first_point_x, first_point_y, railway["rails"][rail]["sides"][side]["x"], railway["rails"][rail]["sides"][side]["y"], first_point_direction, railway["rails"][rail]["sides"][side]["direction"], lineWidth, scale)
                }
            }
            else
            {
                if (first_point)
                {

                    var first_point_x = railway["rails"][rail]["sides"][side]["x"];
                    var first_point_y = railway["rails"][rail]["sides"][side]["y"];
                    first_point = false;
                }
                else
                {
                    console.log("Drawing straigth line from:" + first_point_x + "," + first_point_y + " to " + railway["rails"][rail]["sides"][side]["x"] + "," + railway["rails"][rail]["sides"][side]["y"])
                    context.beginPath();
                    context.moveTo(first_point_x,convertY(first_point_y));
                    context.lineTo(railway["rails"][rail]["sides"][side]["x"], convertY(railway["rails"][rail]["sides"][side]["y"]));
                    context.lineWidth = lineWidth;
                    context.strokeStyle = 'purple';
                    context.stroke();
                    context.closePath();
                }

            }
        }

    }

    // Draw separation between rail:
    for (var rail in railway["rails"]) //Parcourir le dictionnaire.
    {
        for (var side in railway["rails"][rail]["sides"])
        {
            var direction = railway["rails"][rail]["sides"][side]["direction"];
            var x = railway["rails"][rail]["sides"][side]["x"];
            var y = railway["rails"][rail]["sides"][side]["y"];
            drawSide(context, x, y, direction, lineWidth);
        }

    }





    // Create fill gradient
    // var gradient = context.createLinearGradient(0, 0, 0, height);
    // gradient.addColorStop(0, "#ffc821");
    // gradient.addColorStop(1, "#faf100");

    // Add a shadow around the object
    // context.shadowBlur = 10;
    // context.shadowColor = "black";

    // Fill the path
    // context.fillStyle = gradient;
    // context.fill();



}