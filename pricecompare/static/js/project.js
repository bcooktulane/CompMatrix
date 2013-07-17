/* Project specific Javascript goes here. */
$(function() {

    $('.slider').slider({
        value: 50,
        slide: function( event, ui ) {
            var elCredit = $(event.target).closest('.class_stats').find('.credit');
            var elPercent = $(event.target).closest('.class_stats').find('.percent');
            var elPremium = $(event.target).closest('.class_stats').find('.premium');
            var elEstimate = $(event.target).closest('.class_stats').find('.estimate');

            var max_debit = parseFloat($(event.target).attr('data-mincredit'));
            var max_credit = parseFloat($(event.target).attr('data-maxcredit'));
                   
            var premium = parseFloat(elPremium.html().replace(',',''));
            var premium_modifier;
            if (ui.value >= 50) {
                var premium_modifier = (((ui.value - 50) * 2) * 0.01) * max_debit;
                var credit = premium * premium_modifier;
                var estimate = premium * (1+premium_modifier);
                elCredit.html(Math.round(credit));
                elEstimate.html(Math.round(estimate));
            } else {
                var premium_modifier = (((ui.value - 50) * 2) * 0.01) * max_credit;
                var credit = premium * premium_modifier;
                var estimate = premium * (1+premium_modifier);
                elCredit.html("(" + Math.round(credit) + ")");
                elEstimate.html(Math.round(estimate));
            }

            elPercent.html( ui.value + '%');
        }
    });
});
