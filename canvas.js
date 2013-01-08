
window.onload = windowReady;

function drawCurved(context, x1, y1, x2, y2, direction1, direction2, radius, lineWidth, scale, color)
{
    var centerX;
    var centerY;
    var startingAngle;
    var endingAngle;
    var counterclockwise = false;
    // Value fixed by vario-system:
    // console.log(x1 + " " + y1);
    // console.log(x2 + " " + y2);
    // console.log(direction1);
    // console.log(direction2);
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
    console.log("Drawing with:" + centerX + "," + centerY + "," + radius + "," + startingAngle + "," + endingAngle + "," + counterclockwise)
    context.arc(centerX, -centerY, radius, startingAngle, endingAngle, counterclockwise);



    context.lineWidth = lineWidth;
    context.strokeStyle = color;

    context.stroke();

    context.closePath();

    // Draw center:
    // context.fillRect(centerX,centerY,4,4);
    // console.log("fill rect: " + centerX + " " + centerY)

}


function drawSide(context, x, y, direction, _length)
{
    var startX;
    var startY;
    var endX;
    var endY;
    var lineWidth = _length / 8;
    var strokeStyle = 'black';
    context.shadowBlur=0;

    if(direction == 0)
    {
        startX = x - (_length / 2);
        startY = y;
        endX = x + (_length / 2);
        endY = y;
    }
    if(direction == 1)
    {
        startX = x - Math.cos(45) * (_length / 2) - Math.round(lineWidth / 1.5);
        startY = y + Math.cos(45) * (_length / 2) + Math.round(lineWidth / 1.5);
        endX = x + Math.cos(45) * (_length / 2) + Math.round(lineWidth / 1.5);
        endY = y - Math.cos(45) * (_length / 2) - Math.round(lineWidth / 1.5);
    }
    if(direction == 2)
    {
        startX = x;
        startY = y - (_length / 2);
        endX = x;
        endY = y + (_length / 2);
    }
    if(direction == 3)
    {
        startX = x - Math.cos(45) * (_length / 2) - Math.round(lineWidth / 1.5);
        startY = y - Math.cos(45) * (_length / 2) - Math.round(lineWidth / 1.5);
        endX = x + Math.cos(45) * (_length / 2) + Math.round(lineWidth / 1.5);
        endY = y + Math.cos(45) * (_length / 2) + Math.round(lineWidth / 1.5);
    }
    if(direction == 4)
    {
        startX = x - (_length / 2);
        startY = y;
        endX = x + (_length / 2);
        endY = y;
    }
    if(direction == 5)
    {
        startX = x - Math.cos(45) * (_length / 2) - Math.round(lineWidth / 1.5);
        startY = y + Math.cos(45) * (_length / 2) + Math.round(lineWidth / 1.5);
        endX = x + Math.cos(45) * (_length / 2) + Math.round(lineWidth / 1.5);
        endY = y - Math.cos(45) * (_length / 2) - Math.round(lineWidth / 1.5);
    }
    if(direction == 6)
    {
        startX = x;
        startY = y - (_length / 2);
        endX = x;
        endY = y + (_length / 2);
    }
    if(direction == 7)
    {
        startX = x - Math.cos(45) * (_length / 2) - (lineWidth / 1.5);
        startY = y - Math.cos(45) * (_length / 2) - (lineWidth / 1.5);
        endX = x + Math.cos(45) * (_length / 2) + (lineWidth / 1.5);
        endY = y + Math.cos(45) * (_length / 2) + (lineWidth / 1.5);
    }

    context.beginPath();
    context.moveTo(startX, -startY);
    context.lineTo(endX, -endY);
    context.lineWidth = lineWidth;
    context.strokeStyle = strokeStyle;
    context.stroke();
    context.closePath();
    context.shadowBlur=30;

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




    var max_x = railway["max_x"];
    var max_y = railway["max_y"];
    var min_x = railway["min_x"];
    var min_y = railway["min_y"];

    var scale = 0.5;

    var lineWidth = 60 * scale;
    var shift_x = 60 * scale + lineWidth * 2;
    var shift_y = 60 * scale + lineWidth * 2;
    var context = document.getElementById("canvasId").getContext("2d");
    var width = (max_x - min_x + shift_x * 2);
    var height = (max_y - min_y + shift_y * 2);
    // var width = 500;
    // var height = 500;
    var first_point;
    var curved;
    var reverted;
    var side;
    var rail;
    var first_point_x;
    var first_point_y;
    var first_point_direction;
    var second_point_direction;
    var second_point_x;
    var second_point_y;
    var radius;
    var count = 0;


    // console.log("shift_x " + shift_x);
    // console.log("shift_y " + shift_y);
    // console.log(railway)


    context.canvas.height = height * scale;
    context.canvas.width = width * scale;



//     context.translate(shift_x, context.canvas.height + shift_y);   // reset where 0,0 is located
//     context.scale(1,-1); // invert
//     context.translate(0, context.canvas.height);
//     context.scale(scale, -scale);
//     context.translate(shift_x, shift_y);


    // context.canvas.height = 500;
    // context.canvas.width = 500;


    drawCanvasOutline(context, scale);
    context.shadowBlur=30;
    context.shadowColor="black";
    context.translate(shift_x/2, context.canvas.height - shift_y/2);
    context.scale(scale, scale);
//     context.scale(scale, scale);





    console.log("canvas height: " + context.canvas.height);
    console.log("canvas width:" + context.canvas.width);








    for (rail in railway["rails"]) //Parcourir le dictionnaire.
    {
        var count = count + 1;
        // console.log(rail);
        first_point = new Boolean(true);
        // context.beginPath();
        curved = railway["rails"][rail]["curved"];
        reverted = railway["rails"][rail]["reverted"];
        radius = railway["rails"][rail]["radius"];
        color = railway["rails"][rail]["color"];
        // console.log(curved);
        // console.log(reverted);
        for (side in railway["rails"][rail]["sides"])
        {
            if (curved)
                {
                if (first_point)
                {
                    first_point_x = railway["rails"][rail]["sides"][side]["x"];
                    first_point_y = railway["rails"][rail]["sides"][side]["y"];
                    first_point_direction = railway["rails"][rail]["sides"][side]["direction"];
                    // context.moveTo(railway["rails"][rail]["sides"][side]["x"],railway["rails"][rail]["sides"][side]["y"],3,3);
                    first_point = false;
                }
                else
                {
                    second_point_direction = railway["rails"][rail]["sides"][side]["direction"];
                    second_point_x = railway["rails"][rail]["sides"][side]["x"];
                    second_point_y = railway["rails"][rail]["sides"][side]["y"];

                    drawCurved(context, first_point_x, first_point_y, second_point_x, second_point_y, first_point_direction, second_point_direction, radius, lineWidth, scale, color)
                }
            }
            else
            {
                if (first_point)
                {

                    first_point_x = railway["rails"][rail]["sides"][side]["x"];
                    first_point_y = railway["rails"][rail]["sides"][side]["y"];
                    first_point = false;
                }
                else
                {
                    second_point_x = railway["rails"][rail]["sides"][side]["x"];
                    second_point_y = railway["rails"][rail]["sides"][side]["y"];
                    console.log("rail: " + rail + ", Drawing straigth line from:" + first_point_x + "," + -first_point_y + " to " + second_point_x + "," + -second_point_y)
                    context.beginPath();
                    context.moveTo(first_point_x,-first_point_y);
                    context.lineTo(second_point_x, -second_point_y);
                    context.lineWidth = lineWidth;
                    context.strokeStyle = color;
                    context.stroke();
                    context.closePath();
                }

            }
        }

    }
    console.log(count);

    // Draw separation between rail:
    for (rail in railway["rails"]) //Parcourir le dictionnaire.
    {
        for (side in railway["rails"][rail]["sides"])
        {
            first_point_direction = railway["rails"][rail]["sides"][side]["direction"];
            first_point_x = railway["rails"][rail]["sides"][side]["x"];
            first_point_y = railway["rails"][rail]["sides"][side]["y"];
            drawSide(context, first_point_x, first_point_y, first_point_direction, lineWidth);
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

