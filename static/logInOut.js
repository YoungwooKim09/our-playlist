function logOut(){
    $.removeCookie($.cookie())
    return location.reload()
}