Date.prototype.addDays = function(days) {
    var dat = new Date(this.valueOf());
    dat.setDate(dat.getDate() + days);
    return dat;
}

var monthsName = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

function AddCalendar(clickfunc, date_available) {
    var mydate = new Date(2004, 0, 1, 5, 2, 2, 2);
    var week = 0;
    var $calendar;
    $calendar = $('div#calendar');
    var month, day;
    for (month = 0; month < 12; month++) {
        $calendar.append('<div class="month" id="'+mydate.getMonth()+'">'+ monthsName[mydate.getMonth()]+'</div>');

        $month = $("#"+mydate.getMonth()+".month");
        for (day = 0; day < 31; day++) {
            if (day % 7 == 0) {
                var weekclass = "week";
                if (day == 28) {
                    weekclass += "-lastrow";
                }
                $month.append('<div class="'+weekclass+'" id=' + mydate.getMonth() + '_' + week + '></div>');
                $week = $("#"+mydate.getMonth() + '_' + week +"."+weekclass);
                week++;
            }
            var dayclass = "day";
            var day_id = ("0" + (mydate.getMonth() + 1)).slice(-2)+ '_' + ("0" + mydate.getUTCDate()).slice(-2);
            //console.log(date_available);
            if (!(day_id in date_available))
                dayclass = "day-notfound";
            else if (date_available[day_id] != 0)
            {
                dayclass = "day-done";
            }
            $week.append('<span class="'+dayclass+'" id='+ day_id +'>'+("0" + mydate.getUTCDate()).slice(-2)+'</span>');
            $day = $("."+dayclass+"#"+("0" + (mydate.getMonth() + 1)).slice(-2)+ '_' + ("0" + mydate.getUTCDate()).slice(-2));
            if (dayclass == "day-done")
            {
                $day.css('background-image', 'url('+date_available[day_id].thumbnail+')');
            }
            $day.on('click', function(e) {
                var $this = $(this);
                //console.log($this.attr("class"));
                if ($this.attr("class") == "day") {
                    $this.removeClass("day");
                    $this.addClass("day-selected");
                    $("#filter").val($("#filter").val() + "f" + $this.attr('id'));
                } else {
                    $this.removeClass("day-selected");
                    $this.addClass("day");
                    $("#filter").val($("#filter").val().replace("f" + $this.attr('id'), ""))
                }
                clickfunc($this);
                console.log($this.attr('id'));
            });
            mydate = mydate.addDays(1);
            if (mydate.getUTCDate() == 1)
                break;                
        }
        
    }
}