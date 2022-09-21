console.log();

const userInfo = (function () {
  let userInfo = {
    user_name: "",
    user_email: "",
  };
  return {
    setUserInfo(name, email) {
      userInfo = {
        user_name: name || userInfo.user_name,
        user_email: email || userInfo.user_email,
      };
    },
    removeUserInfo() {
      userInfo = {
        user_name: "",
        user_email: "",
      };
    },
    getUserInfo() {
      return userInfo;
    },
  };
})();

console.log(userInfo.getUserInfo());
