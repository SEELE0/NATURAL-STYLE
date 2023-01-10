var jpghd = angular.module('jpghd', ['angularFileUpload', 'ngSanitize']);
jpghd.directive("dropzone", function() {
    return {
        restrict : "A",
        link: function (scope, elem, attr) {
            elem.bind('dragover', function(e) {
                e.stopPropagation();
                e.preventDefault();
            });
            elem.bind('dragenter', function(e) {
                e.stopPropagation();
                e.preventDefault();
            });
            elem.bind('drop', function(e) {
                e.stopPropagation();
                e.preventDefault();
                scope[attr.dropzone](e.dataTransfer.files);
            });
        }
    }
});

var show_alert = function (msg, type, show_buy) {
    $("#modal_alert_text").html(msg);
    $("#modal_alert_button").removeClass().addClass("btn btn-" + type);
    if(show_buy) {
        $("#modal_alert_button").hide();
        $("#modal_alert_show_buy").show();
    } else {
        $("#modal_alert_button").show();
        $("#modal_alert_show_buy").hide();
    };
    $("#modal_alert").modal();
};

var get_suffix = function (f) {
    return (f.lastIndexOf('.')!=-1)?f.substring(f.lastIndexOf('.')):'';
};

var calculate_object_name = function (filename){
    var d = new Date();
    return 'upload/' + d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate() + '/' + d.getTime() + Math.random() + get_suffix(filename);
};

var URL = window.URL || window.webkitURL;
var c1 = new OSS.Wrapper({accessKeyId: 'LTAI4Fy32Wt3ngDnRoHzoa7V',accessKeySecret: 'mIGzVQpJT62RSX4gxd17I4tkUFFdOR',endpoint: 'https://oss-accelerate.aliyuncs.com',bucket: 'jpghd'});

var serialize = function (obj) {
    var str = [];
    for(var p in obj) {
        if(obj[p]===undefined) {
            obj[p] = '';
        };
        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
    }
    return str.join("&");
};

jpghd.controller('ctl_main', function($scope, $rootScope, $http, $upload, $interval) {
    if(location.href.indexOf('reset_active=')!==-1) $("#active-page").modal();

    $scope.is_mobile = /android|webos|iphone|ipad|ipod|blackberry/.test(navigator.userAgent.toLowerCase());
    $scope.is_wechat = /micromessenger/.test(navigator.userAgent.toLowerCase());
    $scope.is_alipay = /alipay/.test(navigator.userAgent.toLowerCase());

    $scope.username = username;
    $scope.lng_dict = lng_dict;
    $scope.ispaid = ispaid;

    $scope.login = function (u, p, r) {
        if(!u || !p) {return false };
        $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
        $http.post(
            "/api/login",
            serialize({'username': u, 'password': p, 'reg': r?'true':''})
        ).success(function(data, status, headers, config) {
            if(data.status === 'password_error') {
                show_alert(lng_dict.login_error, 'danger');
            } else if (data.status === 'not_exist') {
                show_alert(lng_dict.not_exist, 'danger');
            } else if (data.status === 'limit') {
                show_alert(lng_dict.password_max_error, 'danger');
            } else if (data.status === 'ok') {
                $scope.username = u;
                $scope.ispaid = data.ispaid;
                $(".modal").modal('hide');
                if($scope.curr_pay) {
                    var pn = $scope.curr_pay.split('@@');
                    $scope.pay(pn[0], pn[1]);
                    $scope.curr_pay = '';
                };
            } else {
                show_alert(lng_dict.alert_error + data.status, 'danger');
            }
        });
    };

    $scope.is_expire = function (d) {
        return new Date() > new Date(d.replace(' ', 'T'));
    };

    $scope.get_user = function () {
        if(!$scope.username) return false;
        $http.get("/api/user").success(function(data, status, headers, config) {
            $scope.bills = data.bills;
            $scope.history_tasks = data.tasks;
            $scope.ispaid = data.ispaid;
        });
    };
    $scope.get_user();

    $scope.show_user = function (tab) {
        $scope.get_user();
        $("#more-page").modal();
        $("#more-page a[href='#"+tab+"']").tab('show');
    };

    $scope.reset = function (u) {
        if(!u) return false;
        $("#reset-page").modal('hide');
        $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
        $http.post("/api/reset", serialize({'username': u})).success(function(data, status, headers, config) {
            if(data.status === 'ok') {
                show_alert(lng_dict.sended, 'success');
            } else {
                show_alert(lng_dict.alert_error + data.status, 'danger')
            };
        });
    };

    $scope.use_sn = function (sn) {
        $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
        $http.post("/api/sn", serialize({'sn': sn})).success(function(data, status, headers, config) {
            if(data.status === 'ok') {
                show_alert(lng_dict.sn_ok, 'success');
                $scope.tmp_sn = '';
                $scope.bills.push(data.bill);
            } else {
                show_alert(lng_dict.sn_error, 'danger')
            };
        });
    };

    $scope.change_password = function (p) {
        $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
        $http.post("/api/user", serialize({'update_password': 'true', 'new_password': p})).success(function(data, status, headers, config) {
            $(".modal").modal('hide');
            if(data.status === 'ok') {
                show_alert(lng_dict.reset_ok, 'success');
                location.href = "/api/logout";
            } else {
                show_alert(lng_dict.alert_error + data.status, 'danger')
            };
        });
    };

    $scope.update_password = function (p) {
        var token = location.href.match(/reset_active=([^&]*)/)[1];

        $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
        $http.post("/api/reset_active", serialize({'token': token, 'new_password': p})).success(function(data, status, headers, config) {
            $("#active-page").modal('hide');
            if(data.status === 'ok') {
                show_alert(lng_dict.reset_ok, 'success');
            } else {
                show_alert(lng_dict.alert_error + data.status, 'danger')
            };
        });
    };

    $scope.filedrop = function (files) {
        $.each(files, function (k, v) {
            var pic = new Image();
            pic.onload = function() {
                $scope.tasks.push({'pic': pic, 'file': v, 'status': 'new', 'limit': !$scope.ispaid&&((pic.naturalWidth>3000)||(pic.naturalHeight>3000)||(v.size>10*1000*1000)), 'percent': 1});
                $scope.$apply();
            };
            pic.src = URL.createObjectURL(v);
        });
    };

    //[{'file':{'src', 'name', 'size'}, 'status', 'limit', 'output':{'jpghd', 'face': [{origin, hd}, ]}, 'tid', 'percent'}]
    $scope.tasks = [];
    $('#image_file').change(function () {
        $scope.filedrop(this.files);
        $('#image_file').val('');
    });

    $scope.retry = function (tid) {
        $.each($scope.tasks, function (k, v) {
            if(v.tid==tid) {v.status = 'process'; v.percent = 5;};
        });
        $.each($scope.history_tasks, function (k, v) {
            if(v.tid==tid) {v.status = 'process'; v.percent = 5;};
        });
        $http.post("/api/task/" + tid).success(function(data, status, headers, config) {
        });
    };

    $scope.del_task_real = function (idx, tid) {
        if(!confirm(lng_dict.sure)) return;
        $scope.history_tasks.splice(idx, 1);
        $http.delete("/api/task/" + tid).success(function(data, status, headers, config) {});
    };

    $scope.del_task = function (idx) {
        if(!confirm(lng_dict.sure)) return;
        $scope.tasks.splice(idx, 1);
    };

    $scope.del_all_task = function () {
        if(!confirm(lng_dict.sure)) return;
        $scope.tasks = [];
    };

    $scope.curr_idx = '';
    $scope.show_start = function (idx) {
        $scope.curr_idx = idx;
        $("#modal_detail").modal();
    };

    $scope.show_scratch = function () {
        $(".modal").modal('hide');
        $("#modal_scratch").modal().on('shown.bs.modal', function () {
            $('#modal_scratch').find('.resize img').css('width', $('#modal_scratch .ba-slider').eq(0).width()+'px');
        });
        return false;
    };

    $scope.tmp_conf = {style: 'photo', scratch: false, x4: false};
    $scope.start = function (idx) {
        if(idx<0 || $scope.tasks[idx].status!=='new') return false;
        var task_create = function (t) {
            $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
            $http.post("/api/task/", serialize({'conf':JSON.stringify({'filename': t.file.name, 'input': t.file.src_url, 'scratch': $scope.tmp_conf.scratch?'ok':'', 'style': (!$scope.tmp_conf.x4&&$scope.tmp_conf.style=='photo')?'photo_slim':$scope.tmp_conf.style})})).success(function(data, status, headers, config) {
                if(data.status === 'ok') {
                    t['tid'] = data.tid;
                } else if (data.status === 'user_not_exist') {
                    $scope.tasks[idx]['status'] = 'new';
                    $scope.tasks[idx]['percent'] = 1;
                    show_alert(lng_dict.user_not_exist, 'danger');
                } else if (data.status === 'conf_param_error') {
                    $scope.tasks[idx]['status'] = 'new';
                    $scope.tasks[idx]['percent'] = 1;
                    show_alert(lng_dict.conf_param_error, 'danger');
                } else if (data.status === 'exceed_limit') {
                    $scope.tasks[idx]['status'] = 'new';
                    $scope.tasks[idx]['percent'] = 1;
                    show_alert(lng_dict.exceed_limit, 'danger', true);
                } else {
                    $scope.tasks[idx]['status'] = 'new';
                    $scope.tasks[idx]['percent'] = 1;
                    show_alert($rootScope.lng_dict.alert_error + data.status, 'danger');
                }
            });
        };
        $scope.tasks[idx]['status'] = 'process';
        $scope.tasks[idx]['percent'] = 5;
        if($scope.tasks[idx].file.src_url) return task_create($scope.tasks[idx]);
        c1.multipartUpload(calculate_object_name($scope.tasks[idx].file.name), $scope.tasks[idx].file).then(function (result) {
            $scope.tasks[idx].file.src_url = result.res.requestUrls[0].split('?')[0];
            task_create($scope.tasks[idx]);
        }).catch(function (err) {
            show_alert(lng_dict.upload_error, 'danger');
        });
    };


    $interval(function() {
        var tids = [];
        $.each($scope.tasks, function (k, v) {
            if(v.status=='process' && v.tid) tids.push(v.tid);
        });
        if(tids.length==0) return false;
        $http.get("/api/task/" + tids.join(',')).success(function(data, status, headers, config) {
            $.each($scope.tasks, function (k, v) {
                if(v.status=='process' && v.tid in data) {
                    if(data[v.tid].status=='success') {
                        v.status = 'success';
                        v.output = data[v.tid].output;
                        v.percent = 100;
                    };
                    if(data[v.tid].status=='error') {
                        v.status = 'error';
                        v.percent = 100;
                    };
                    if(data[v.tid].status=='process' || data[v.tid].status=='new') {
                        v.status = 'process';
                        v.percent<97?(v.percent += 1):'';
                    };
                };
            });
        });
    }, 5000);

    $scope.download_all = function (output) {
        var i = 0;
        $.each(output, function (k, v) {
            i++;
            setTimeout(function (url) {
                var a = document.createElement("a");
                a.setAttribute('href', url);
                a.setAttribute('download', '');
                a.click();
            }, i*500, v);
        });
    };

    $scope.num_price = function (num, lng) {
        var bl = Object.keys(num_bonus);
        bl.sort(function (a, b) {return parseInt(b)-parseInt(a);})
        bonus = 1
        for(var i in bl) {
            if(num >= parseInt(bl[i])) {
                bonus = num_bonus[parseInt(bl[i])];
                break;
            };
        };
        return [Math.ceil(bonus*num), (lng=='zh'?'￥':'$')+((lng=='zh'?0.6:0.1)*num).toFixed(2)];
    };

    $scope.pay_cache = {};//{num: {expire, qr, url}}
    $scope.curr_pay_type = '';
    $scope.pay_qr = '';
    $scope.pay_url = '';
    $scope.curr_pay = '';
    $scope.pay = function (pay_type, num) {
        if(!$scope.username) {
            $(".modal").modal('hide');
            $("#login-page").modal();
            $scope.curr_pay = pay_type + '@@' + num;
            return false;
        };
        if(!num || num<30) {
            show_alert(lng_dict.min_num, 'danger');
            return false;
        };
        if(pay_type=='paypal') {
            window.location = '/api/paypal_order?n='+num+'&u='+$scope.username;
            return false;
        };
        var k = pay_type + num;
        var now = new Date();
        $scope.curr_pay_type = pay_type;
        $scope.pay_qr = '';
        $scope.pay_url = '';

        if($scope.pay_cache[k] && $scope.pay_cache[k]['expire'] > now) {
            $scope.pay_qr = $scope.pay_cache[k]['qr'];
            $scope.pay_url = $scope.pay_cache[k]['url'];
        } else {
            $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
            $http.post("/api/bill", serialize({'u': $scope.username, 'a': pay_type=='alipay'?'1':'', 'n': num})).success(function(data, status, headers, config) {
                if(data.status === 'ok') {
                    now.setMinutes(now.getMinutes() + 5);
                    $scope.pay_cache[k] = {'expire': now, 'qr': data.qr, 'url': data.qr_url};
                    $scope.pay_qr = $scope.pay_cache[k]['qr'];
                    $scope.pay_url = $scope.pay_cache[k]['url'];
                } else {
                    show_alert(lng_dict.alert_error + data.status, 'danger');
                };
            });
        };
        $(".modal").modal('hide');
        $("#modal_pay").modal();
    };

    $scope.formatBytes = function (a,b){if(0==a)return"0 Bytes";var c=1e3,d=b||2,e=["Bytes","KB","MB","GB","TB","PB","EB","ZB","YB"],f=Math.floor(Math.log(a)/Math.log(c));return parseFloat((a/Math.pow(c,f)).toFixed(d))+" "+e[f]};

});
