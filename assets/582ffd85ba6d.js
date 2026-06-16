$(function () {
    $('.form1').on('click', '.send1', function (event) {
        event.preventDefault();
        var jForm = $(event.delegateTarget), jThis = $(this);
        if (jThis.hasClass('disabled')) {
            alert('Please wait...');
            return;
        }

        var reg_email = /^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$/;

        var data = {
            id: 'bottomemail', _spam: '{$session.project_spam}',
            title: $('input[name="title"]', jForm).val().trim(),
            email: $('input[name="email"]', jForm).val().trim(),
        };


        if (!data.email || !reg_email.test(data.email)) {
            alert('Please enter a valid email address.');
            // alert('请输入一个有效的邮箱地址');
            $('input[name="email"]', jForm).focus();
            return false;
        }



        jThis.css({opacity: '.5'}).addClass('disabled');

        $.ajax({
            'url' : '/api.php?c=post&f=save&_t='+(new Date().getTime()),
            'data': jForm.serializeArray(),
            'type' : 'post',
            'dataType' : 'json',
            'success' : function (rs) {
                jThis.css({opacity: '1'}).removeClass('disabled');
                if (rs.status == 'ok') {
                    // alert('Your message has been posted, please wait patiently administrator audit, thank you for your submission');
                    // alert('您的留言已提交,请耐心等候管理员回复');
                    if (jForm.hasClass('form1')) {
                        location.href = '/messagetrue.html';
                    } else {
                        jForm.get(0).reset();
                    }
                } else {
                    alert(rs.content);
                    return false;
                }
            }
        });
        return false;
    });
});


$(function () {
    $('.form2').on('click', '.send2', function (event) {
        event.preventDefault();
        var jForm = $(event.delegateTarget), jThis = $(this);
        if (jThis.hasClass('disabled')) {
            alert('Please wait...');
            return;
        }

        var reg_email = /^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$/;

        var data = {
            id: 'book', _spam: '{$session.project_spam}',
            title: $('input[name="title"]', jForm).val().trim(),
            fullname: $('input[name="fullname"]', jForm).val().trim(),
            email: $('input[name="email"]', jForm).val().trim(),
            content: $('textarea[name="content"]', jForm).val().trim(),
        };


        if (!data.email || !reg_email.test(data.email)) {
            alert('Please enter a valid email address.');
            // alert('请输入一个有效的邮箱地址');
            $('input[name="email"]', jForm).focus();
            return false;
        } else if (!data.title) {
            alert('The Subject cannot be empty.');
            // alert('请输入留言主题');
            $('input[name="title"]', jForm).focus();
            return false;
        } else if (!data.content) {
            alert('The message cannot be empty.');
            // alert('请输入留言内容');
            $('textarea[name="content"]', jForm).focus();
            return false;
        } else if (!data.fullname) {
            alert('The name cannot be empty.');
            // alert('请输入姓名');
            $('input[name="fullname"]', jForm).focus();
            return false;
        }


        jThis.css({opacity: '.5'}).addClass('disabled');

        $.ajax({
            'url' : '/api.php?c=post&f=save&_t='+(new Date().getTime()),
            'data': jForm.serializeArray(),
            'type' : 'post',
            'dataType' : 'json',
            'success' : function (rs) {
                jThis.css({opacity: '1'}).removeClass('disabled');
                if (rs.status == 'ok') {
                    // alert('您的留言已提交,请耐心等候管理员回复');
                    if (jForm.hasClass('form2')) {
                    // alert('Your message has been posted, please wait patiently administrator audit, thank you for your submission');
                        location.href = '/messagetrue.html';
                    } else {
                        jForm.get(0).reset();
                    }
                } else {
                    alert(rs.content);
                    return false;
                }
            }
        });
        return false;
    });
});


$(function () {
    $('.form3').on('click', '.send3', function (event) {
        event.preventDefault();
        var jForm = $(event.delegateTarget), jThis = $(this);
        if (jThis.hasClass('disabled')) {
            alert('Please wait...');
            return;
        }

        var reg_email = /^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$/;

        var data = {
            id: 'book', _spam: '{$session.project_spam}',
            title: $('input[name="title"]', jForm).val().trim(),
            fullname: $('input[name="fullname"]', jForm).val().trim(),
            email: $('input[name="email"]', jForm).val().trim(),
            content: $('textarea[name="content"]', jForm).val().trim(),
        };


        if (!data.email || !reg_email.test(data.email)) {
            alert('Please enter a valid email address.');
            // alert('请输入一个有效的邮箱地址');
            $('input[name="email"]', jForm).focus();
            return false;
        } else if (!data.title) {
            alert('The Subject cannot be empty.');
            // alert('请输入留言主题');
            $('input[name="title"]', jForm).focus();
            return false;
        } else if (!data.content) {
            alert('The message cannot be empty.');
            // alert('请输入留言内容');
            $('textarea[name="content"]', jForm).focus();
            return false;
        } else if (!data.fullname) {
            alert('The name cannot be empty.');
            // alert('请输入姓名');
            $('input[name="fullname"]', jForm).focus();
            return false;
        }


        jThis.css({opacity: '.5'}).addClass('disabled');

        $.ajax({
            'url' : '/api.php?c=post&f=save&_t='+(new Date().getTime()),
            'data': jForm.serializeArray(),
            'type' : 'post',
            'dataType' : 'json',
            'success' : function (rs) {
                jThis.css({opacity: '1'}).removeClass('disabled');
                if (rs.status == 'ok') {
                    // alert('您的留言已提交,请耐心等候管理员回复');
                    if (jForm.hasClass('form3')) {
                    // alert('Your message has been posted, please wait patiently administrator audit, thank you for your submission');
                        location.href = '/messagetrue.html';
                    } else {
                        jForm.get(0).reset();
                    }
                } else {
                    alert(rs.content);
                    return false;
                }
            }
        });
        return false;
    });
});
