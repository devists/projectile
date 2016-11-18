/**
 * Created by ansarimofid on 06/11/16.
 */
$(document).ready(function () {
    $('.ui.dropdown').dropdown();
    $('.ui.checkbox').checkbox()
})


$(document).ready(function () {
    $('#demo-pie-1').pieChart({
        barColor: '#68b828',
        trackColor: '#eee',
        lineCap: 'round',
        lineWidth: 8,
        onStep: function (from, to, percent) {
            $(this.element).find('.pie-value').text(Math.round(percent) + '%');
        }
    });

    $('#demo-pie-2').pieChart({
        barColor: '#8465d4',
        trackColor: '#eee',
        lineCap: 'butt',
        lineWidth: 8,
        onStep: function (from, to, percent) {
            $(this.element).find('.pie-value').text(Math.round(percent) + '%');
        }
    });

    $('#demo-pie-3').pieChart({
        barColor: '#457303',
        trackColor: '#eee',
        lineCap: 'square',
        lineWidth: 8,
        onStep: function (from, to, percent) {
            $(this.element).find('.pie-value').text(Math.round(percent) + '%');
        }
    });

    $('#demo-pie-4').pieChart({
        barColor: '#8465d4',
        trackColor: '#eee',
        lineCap: 'round',
        lineWidth: 8,
        rotate: 90,
        onStep: function (from, to, percent) {
            $(this.element).find('.pie-value').text(Math.round(percent) + '%');
        }
    });
    $('#demo-pie-5').pieChart({
        barColor: '#8465d4',
        trackColor: '#eee',
        lineCap: 'round',
        lineWidth: 8,
        rotate: 90,
        onStep: function (from, to, percent) {
            $(this.element).find('.pie-value').text(Math.round(percent) + '%');
        }
    });
    $('#demo-pie-6').pieChart({
        barColor: '#8465d4',
        trackColor: '#eee',
        lineCap: 'round',
        lineWidth: 8,
        rotate: 90,
        onStep: function (from, to, percent) {
            $(this.element).find('.pie-value').text(Math.round(percent) + '%');
        }
    });


    $.get('/inbox/notifications/api/unread_count/',function (data) {
        console.log("Notification");
        console.log(data.unread_count);
        if(data.unread_count) {
            var notify =  $('.notify .label-container');
            $('.notify').addClass('color-primary').removeClass('color-g97');
            notify.find('.ui.label').text(data.unread_count);
            notify.show();

            console.log(data.unread_count+" New Notification");
        }
        console.log(data);
    })

});
