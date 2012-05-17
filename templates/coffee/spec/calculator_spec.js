(function() {

  describe('Calculator', function() {
    beforeEach(function() {
      loadFixtures('calculator.html');
      return this.calculator = new Calculator;
    });
    describe('bind', function() {
      beforeEach(function() {
        return Calculator.bind();
      });
      it('bind the calculator button', function() {
        return expect($('.calc')).toHandleWith('click', this.calculator.toggle);
      });
      it('bind the help button', function() {
        expect($('div.help-wrapper a')).toHandleWith('mouseenter', this.calculator.helpToggle);
        return expect($('div.help-wrapper a')).toHandleWith('mouseleave', this.calculator.helpToggle);
      });
      it('prevent default behavior on help button', function() {
        $('div.help-wrapper a').click(function(e) {
          return expect(e.isDefaultPrevented()).toBeTruthy();
        });
        return $('div.help-wrapper a').click();
      });
      it('bind the calculator submit', function() {
        return expect($('form#calculator')).toHandleWith('submit', this.calculator.calculate);
      });
      return it('prevent default behavior on form submit', function() {
        $('form#calculator').submit(function(e) {
          expect(e.isDefaultPrevented()).toBeTruthy();
          return e.preventDefault();
        });
        return $('form#calculator').submit();
      });
    });
    describe('toggle', function() {
      it('toggle the calculator and focus the input', function() {
        spyOn($.fn, 'focus');
        this.calculator.toggle();
        expect($('li.calc-main')).toHaveClass('open');
        return expect($('#calculator_wrapper #calculator_input').focus).toHaveBeenCalled();
      });
      return it('toggle the close button on the calculator button', function() {
        this.calculator.toggle();
        expect($('.calc')).toHaveClass('closed');
        this.calculator.toggle();
        return expect($('.calc')).not.toHaveClass('closed');
      });
    });
    describe('helpToggle', function() {
      return it('toggle the help overlay', function() {
        this.calculator.helpToggle();
        expect($('.help')).toHaveClass('shown');
        this.calculator.helpToggle();
        return expect($('.help')).not.toHaveClass('shown');
      });
    });
    return describe('calculate', function() {
      beforeEach(function() {
        $('#calculator_input').val('1+2');
        spyOn($, 'getJSON').andCallFake(function(url, data, callback) {
          return callback({
            result: 3
          });
        });
        return this.calculator.calculate();
      });
      it('send data to /calculate', function() {
        return expect($.getJSON).toHaveBeenCalledWith('/calculate', {
          equation: '1+2'
        }, jasmine.any(Function));
      });
      return it('update the calculator output', function() {
        return expect($('#calculator_output').val()).toEqual('3');
      });
    });
  });

}).call(this);
