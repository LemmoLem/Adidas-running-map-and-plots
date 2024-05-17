//js to change colour of the run when user hovers mouse over
//if a run is clicked it changes colour and is brought to front
//also adds navbar

var layerClickedLast = null;
document.addEventListener('DOMContentLoaded', function () {
    var mapElement = document.querySelector('.folium-map').id;
    var mapInstance = window[mapElement];
    mapInstance.eachLayer(function (layer) {
        if (layer instanceof L.Polyline) {
            layer.on('mouseover', function (e) {
                if (layer != layerClickedLast){
                    layer.setStyle({ color: 'blue', weight: 3 });
                }
                else{
                    layerClickedLast.setStyle({ color: 'lightGreen', weight: 5 });
                }
            });       
            layer.on('mouseout', function (e) {
                if (layer != layerClickedLast){
                    layer.setStyle({ color: '#FF0000', weight: 1.0 });
                }
                else{
                    layerClickedLast.setStyle({ color: 'green',  weight: 4 });
                }
            });
            layer.on('click', function (e) {
                if (layerClickedLast != null){
                    layerClickedLast.setStyle({ color: '#FF0000', weight: 0.8});
                }
                layer.setStyle({ color: 'green',  weight: 4 });
                layer.bringToFront();
                layerClickedLast = layer;
            });
        }
    });
});

var div = document.createElement("div");
div.className = "navbar"
var link1 = document.createElement("a");
link1.href = "foliumMap.html";
link1.textContent = "MAP";

var link2 = document.createElement("a");
link2.href = "index.html";
link2.textContent = "PLOTS";

div.appendChild(link1);
div.appendChild(link2);

document.body.insertBefore(div, document.body.firstChild);
