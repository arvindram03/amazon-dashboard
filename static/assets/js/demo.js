type = ['','info','success','warning','danger'];
    	

demo = {
    initPickColor: function(){
        $('.pick-class-label').click(function(){
            var new_class = $(this).attr('new-class');  
            var old_class = $('#display-buttons').attr('data-class');
            var display_div = $('#display-buttons');
            if(display_div.length) {
            var display_buttons = display_div.find('.btn');
            display_buttons.removeClass(old_class);
            display_buttons.addClass(new_class);
            display_div.attr('data-class', new_class);
            }
        });
    },
    initBubblePlot: function(review_time) {
      
      $(function () {
          var review_data = [];
          for (var i=0;i<review_time.length;i++) {
            parts = review_time[i].toString().split(",");
            review_data.push({ x: parseInt(parts[0]), y: parseInt(parts[1]), z: parseInt(parts[1]), name: parts[1], country: '' });
          }
          for (var i=0;i<review_time.length;i++) {
            console.log(review_data[i]);
          }
          $('#reviewTime').highcharts({

              chart: {
                  type: 'bubble',
                  plotBorderWidth: 1,
                  zoomType: 'xy'
              },

              legend: {
                  enabled: false
              },

              title: {
                  text: 'Review count across years'
              },

              xAxis: {
                  gridLineWidth: 0,
                  tickInterval: 1,
                  title: {
                      text: 'Year'
                  },
                  labels: {
                      format: '{value}'
                  }
              },

              yAxis: {
                  startOnTick: false,
                  endOnTick: false,
                  title: {
                      text: 'Review Count'
                  },
                  labels: {
                      format: '{value} reviews'
                  },
                  maxPadding: 0.2
              },
              plotOptions: {
                  series: {
                      dataLabels: {
                          enabled: true,
                          format: '{point.name}'
                      }
                  }
              },
              series: [{
                  data: review_data
              }]

          });
      });
    },
    initBarPlot: function(review_data) {
         $(function () {
            $('#reviewChart').highcharts({
                chart: {
                    type: 'bar'
                },
                title: {
                    text: 'Review Distribution'
                },
                xAxis: {
                    categories: ['1 reviews', '2 reviews', '3 reviews', '4 reviews', '5 reviews'],
                    title: {
                        text: null
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Review count',
                        align: 'high'
                    },
                    labels: {
                        overflow: 'justify'
                    }
                },
                tooltip: {
                    valueSuffix: ' reviews'
                },
                plotOptions: {
                    bar: {
                        dataLabels: {
                            enabled: true
                        }
                    }
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'top',
                    x: -40,
                    y: 80,
                    floating: true,
                    borderWidth: 1,
                    backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
                    shadow: true
                },
                credits: {
                    enabled: false
                },
                series: [{
                    name: 'Reviews',
                    data: [review_data[1], review_data[2], review_data[3], review_data[4], review_data[5]]
                }]
            });
        }); 
    },
    initBoxPlot: function(box_data) {
      //var obs_data = JSON.parse(box_data)
      $('#chartHours').highcharts({
          chart: {
              type: 'boxplot'
          },
          title: {
              text: 'Highcharts Box Plot Example'
          },
          legend: {
              enabled: true
          },
          xAxis: {
              categories: ['1', '2', '3', '4', '5'],
              title: {
                  text: 'Experiment No.'
              }
          },
          yAxis: {
              title: {
                  text: 'Observations'
              },
              plotLines: [{
                  value: 932,
                  color: 'red',
                  width: 1,
                  label: {
                      text: 'Theoretical mean: 932',
                      align: 'center',
                      style: {
                          color: 'gray'
                      }
                  }
              }]
          },
          series: [{
              name: 'Observations',
              data: box_data.data,
              tooltip: {
                  headerFormat: '<em>Experiment No {point.key}</em><br/>'
              }
          }, {
              name: 'Outlier',
              color: Highcharts.getOptions().colors[0],
              type: 'scatter',
              data: box_data.outlier_data,
              marker: {
                  fillColor: 'white',
                  lineWidth: 1,
                  lineColor: Highcharts.getOptions().colors[0]
              },
              tooltip: {
                  pointFormat: 'Observation: {point.y}'
              }
          }]

      });
      
    },

    initSparkline: function(uid,review_day) {
        $('#chartPreferences').highcharts({
        chart: {
            type: 'areaspline'
        },
        title: {
            text: 'Review Distribution across days of week'
        },
        xAxis: {
            categories: [
                'Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday',
                'Sunday'
            ],
            plotBands: [{ // visualize the weekend
                from: 4.5,
                to: 6.5,
                color: 'rgba(68, 170, 213, .2)'
            }]
        },
        yAxis: {
            title: {
                text: 'Review Percentage'
            }
        },
        tooltip: {
            shared: true,
            valueSuffix: ' units'
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            areaspline: {
                fillOpacity: 0.5
            }
        },
        series: [{
            name: 'Overall Average',
            data: [15, 13, 14, 13, 15, 14, 13]
        }, {
            name: uid,
            data: [review_day[0]*100, review_day[1]*100, review_day[2]*100, review_day[3]*100, review_day[4]*100, review_day[5]*100, review_day[6]*100]
        }]
    });
    },
    
  	showNotification: function(from, align){
      	color = Math.floor((Math.random() * 4) + 1);
      	
      	$.notify({
          	icon: "pe-7s-gift",
          	message: "Welcome to <b>Light Bootstrap Dashboard</b> - a beautiful freebie for every web developer."
          	
          },{
              type: type[color],
              timer: 4000,
              placement: {
                  from: from,
                  align: align
              }
          });
  	}

    
}

