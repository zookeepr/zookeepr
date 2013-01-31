// From http://jsfiddle.net/IgorMinar/mVSPC/ - Twitter bootstrap modal dialog widget (0.10.7, Igor Minar)

dialogApp = angular.module('dialog', []);

dialogApp.directive('bsDialog', function($templateCache, $document, $compile) {
  return {
    terminal: true,
    link: function(scope, element, attrs) {
      var dialogElement,
          dialogBodyElement,
          dialogScope,
          dialogBodyScope,
          dialogBodyTemplate = element.contents();

      element.remove();

      scope.$watch(attrs.when, function(show) {
        if (show) {
          dialogScope = scope.$new(); // maybe even use $rootScope instead
          dialogBodyScope = scope.$new(); // must be child of scope => no need to export model

          angular.extend(dialogScope, {
            title: attrs.title,
            primaryLabel: attrs.primaryLabel || 'OK',
            secondaryLabel: attrs.secondaryLabel || 'Cancel',
            closeDialog: function() {
              dialogElement.modal('hide');
            },
            primaryAction: function() {
              this.closeDialog();
              dialogBodyScope.$eval(attrs.primaryAction);
            },
            secondaryAction: function() {
              this.closeDialog();
              dialogBodyScope.$eval(attrs.secondaryAction);
            }
          });

          dialogElement = $($templateCache.get('dialog-template'));
          $document.append(dialogElement);
          $compile(dialogElement)(dialogScope);
          dialogBodyElement = dialogElement.find('.modal-body');
          dialogBodyElement.append(dialogBodyTemplate);
          $compile(dialogBodyElement)(dialogBodyScope);

          dialogElement.modal('show');
          dialogElement.bind('hidden', function() {
            scope.$apply(function() {
              dialogScope.$destroy();
              dialogBodyScope.$destroy();
              dialogElement.remove();
              dialogElement = null;
              scope[attrs.when] = false; //hack, the model might be on a upper scope or might be a fn
            });
          });
        } else {
          if (dialogElement) {
            dialogElement.modal('hide');
          }
        }
      });
    }
  }
});
