'use strict';

/**
 * @ngdoc service
 * @name frontendApp.BackendService
 * @description
 * # BackendService
 * Service in the frontendApp.
 */
angular.module('frontendApp')
  .service('BackendService', function ($http, $log) {
    var service = this;
    //var baseUrl = 'http://10.0.150.54:8080/api/v1/';
    var baseUrl = 'http://127.0.0.1:8080/api/v1/';
    this.merchants = [];
    this.transactions = [];
    this.selectedMerchant = {active: null};

    this.initialize = function(){
      return $http({
        url: baseUrl + 'brands',
        method: 'get'
      }).then(function(response){
        service.merchants = response.data.list;
        if (service.merchants && service.merchants.length > 0)
          service.selectedMerchant.active = service.merchants[0];
      }, function(error){
        $log.debug(error);
      });
    };

    this.listTransactions = function(params){
      return $http({
        url: baseUrl + 'transactions',
        method: 'get',
        params: params
      })
    }
  });
