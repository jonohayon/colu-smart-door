var app = angular.module('smartDoor', ['ngMaterial'])
var userDetails

// Use in case of emergency
app.controller('qrCtrl', function ($scope, $http) {
  $scope.register = function () {
    $scope.form = {
      firstName: $scope.firstName,
      lastName: $scope.lastName,
      phone: $scope.phoneNumber,
      email: $scope.email,
      username: $scope.username,
      type: $scope.type
    }
    $http.post('/api/get_qr?token=' + sessionStorage.adminToken, $scope.form).success(function (data, status, headers, config) {
      $scope.qrCode = data.base64data
      $http.post('/api/signup?token=' + sessionStorage.adminToken, { regMsg: data.regMsg, code: data.code, user: data.user }).success(function (data, status, headers, config) {
        console.log(data)
      })
    })
  }
  $scope.login = function () {
    $http.post('/api/login', { userName: $scope.firstName + ' ' + $scope.lastName }).success(function (data, status, headers, config) {
      console.log(data)
    })
  }
})

app.controller('navCtrl', function ($scope, $http) {
  var route = window.location.pathname.replace('/', '')
  $scope.isList = false
  if (route === 'list') {
    $scope.isList = true
  } else {
    $scope.isList = false
  }
  $scope.isSearch = false
  $scope.openSearch = function () {
    $scope.isSearch = true
  }
  $scope.closeSearch = function () {
    $scope.isSearch = false
  }
})

app.controller('loginCtrl', function ($scope, $http) {
  $scope.login = function () {
    if ($scope.username === null || !$scope.username || $scope.username === undefined || $scope.username === '') {
      alert('Username is required')
    } else {
      console.log($scope.username)
      $http.post('/api/adlog', { username: $scope.username }).success(function (data, status, headers, config) {
        console.log(data)
        if (data.message === 'Admin verified') {
          sessionStorage.adminToken = data.token
          window.location.href = '/list?token=' + sessionStorage.adminToken
        }
      })
    }
  }
})

app.controller('tableCtrl', function ($scope, $http, $mdDialog) {
  $http.get('/api/get_users').success(function (data, status, config, headers) {
    $scope.users = data
    $scope.usersNum = $scope.users.length
  })
  setInterval(function () {
    $http.get('/api/get_users').success(function (data, status, config, headers) {
      console.log('Admin token:', sessionStorage.adminToken)
      $scope.users = data
      $scope.usersNum = data.length
    })
  }, 600000)
  $scope.isDelHover = false
  $scope.delHover = function (bool) {
    console.log(bool)
    $scope.isDelHover = bool
    return bool
  }
  $scope.showInfo = function (ev, user) {
    if (!$scope.isDelHover) {
      userDetails = user
      $mdDialog.show({
        controller: userDialogCtrl,
        templateUrl: 'templates/userDialog.html',
        parent: angular.element(document.body),
        targetEvent: ev
      })
    }
  }
  $scope.showAddUser = function (ev) {
    $mdDialog.show({
      controller: addUserCtrl,
      templateUrl: 'templates/addDialog.html',
      parent: angular.element(document.body),
      targetEvent: ev
    })
  }
  $scope.deleteUser = function (ev, user) {
    userDetails = user
    $mdDialog.show({
      controller: deleteDialogCtrl,
      templateUrl: 'templates/deleteDialog.html',
      parent: angular.element(document.body),
      targetEvent: ev
    })
  }
})

app.controller('intercomCtrl', function ($scope, $http, $mdDialog) {
  $http.get('/api/get_users').success(function (data, status, config, headers) {
    $scope.users = data
    $scope.usersNum = $scope.users.length
  })
  setInterval(function () {
    $http.get('/api/get_users').success(function (data, status, config, headers) {
      $scope.users = data
      $scope.usersNum = data.length
    })
  }, 600000)
  $scope.ring = function (ev, user) {
    userDetails = user
    $mdDialog.show({
      controller: loadingCtrl,
      templateUrl: 'templates/loadingDialog.html',
      parent: angular.element(document.body),
      targetEvent: ev
    })
  }
})

function userDialogCtrl ($scope, $mdDialog) {
  $scope.user = userDetails
  $scope.hide = function () {
    $mdDialog.hide()
  }
}

function deleteDialogCtrl ($scope, $mdDialog, $http) {
  $scope.user = userDetails
  $scope.message = 'Are you sure you want to delete ' + $scope.user.firstName + ' ' + $scope.user.lastName + '?'
  $scope.hide = function () {
    $mdDialog.hide()
  }
  $scope.deleteUser = function (user) {
    $http.post('/api/delete_user?token=' + sessionStorage.adminToken, user).success(function (data, status, headers, config) {
      if (data.message === 'Deleted ' + user.firstName + ' ' + user.lastName + ' from the DB') {
        $scope.message = 'Deleted ' + user.firstName + ' ' + user.lastName + ' from the DB'
      }
    })
  }
}

function addUserCtrl ($scope, $mdDialog, $http) {
  $scope.hide = function () {
    $mdDialog.hide()
  }
  $scope.addUser = function () {
    $scope.isDone = false
    $scope.form = {
      firstName: $scope.firstName,
      lastName: $scope.lastName,
      phone: $scope.phoneNumber,
      email: $scope.email,
      type: 'user'
    }
    $http.post('/api/get_qr?token=' + sessionStorage.adminToken, $scope.form).success(function (data, status, headers, config) {
      $scope.isQr = true
      $scope.qrCode = data.base64data
      $http.post('/api/signup?token=' + sessionStorage.adminToken, { regMsg: data.regMsg, code: data.code, user: data.user }).success(function (data, status, headers, config) {
        if (data.message === 'User registered') {
          $scope.isQr = false
          $scope.isDone = true
        }
      })
    })
  }
}

function loadingCtrl ($scope, $http, $mdDialog) {
  $scope.cancel = function () {
    $mdDialog.cancel()
  }
  $http.post('/api/login', { userName: userDetails.firstName + ' ' + userDetails.lastName }).success(function (data, status, headers, config) {
    console.log(data)
    $mdDialog.cancel()
  })
}
