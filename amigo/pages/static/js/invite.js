$(document).ready(function() {
    var inputedMessages = {
        accept: '',
        decline: ''
    }

    var acceptResponses = [
        "Yaaaaasss! Dropping everything, I’ll be there.",
        "Best invitation since prom, I’m there!",
        "Was gonna finish my puzzle, but I’ll join you.",
        "I’ll be there, so much to gossip about",
        "Already here spying on you from behind a potted plant.",
        "I'm in but this time, I’d better not get arrested.",
        "I’m coming, and so’s my mom she worries about you.",
        "I’ll be there, unless I get a better offer.",
        "You lit my bat signal. I'll be there",
        "I’m coming, def more fun than watching LOLcat videos",
        "Totally down, just don’t tell my mom.",
        "Even an Uber surge couldn’t keep me from this party.",
        "Count me in, I finally caught up with the Kardashians.",
        "Sounds way more fun than chatting up the bus driver.", 
        "Anyone who’s anyone will be there, and I'm anyone!",
        "I’ll be there, we have to work on quarterly squad goals.",
        "I’ll be there AND watch ur drink while ur in the bathroom.",
        "I’ll be there, please do the wave when I walk in.",
        "I’m the Thelma to your Louise of course I’ll be there.",
        "I’ll be there, I was just starting to bore the cat.",
        "I’ll be there AND be your getaway driver.",
        "I’m the Laverne to your Shirley, of course I’ll be there.",
        "I’m the Chandler to your Ross, of course I’ll be there.",
        "Sounds cheaper than our shopping trips, I’ll be there.",
        "This def sounds funner than going to Chuck e Cheese drunk.",
        "I'm in, sounds like something to put on our gravestone.",
        "Yes, can’t wait to tell my grandkids about this.",
        "How did u know I was free? Did I leave my webcam on again?",
        "I’m in, but send the elves to clean my apt while we're out",
        "I’m there, what are your other 2 wishes?",
        "Yes, def be there for your surprise par---whoops!",
        "Yes, let’s paint the town red! Won’t bring paint this time",
        "Yes, I bought a dress just for this, well I’m about to...",
        "Yes!  Definitely need some fresh selfies!",
        "Sure, this is just an excuse to get drinks after, right?",
        "I’m coming, and I’ll skip the whole way there.",
        "I’ll be there, producing and filming your snapchats.",
        "I’ll be there, filtering the instas until you're engaged."
    ];

    var rejectResponses = [
        "I can't make it, but thanks for thinking of me.",
        "Sorry, I have a conflict. Hope to see you soon!",
        "Thanks for thinking of me, hope I can next time.",
        "I can’t join you, I’m in jail, have you got bail?",
        "Can't make it, half way thru a season of House of Cards.",
        "New phone, who dis?",
        "Wish I could! I have 127 socks, and need to match them up.",
        "Sorry, a wizard just told me to chuck a ring in a volcano.",
        "Can't make it I’m getting married, and I don’t know who to.",
        "Sorry, stuck in a labyrinth arguing with the King of Goblins",
        "Can't make it, have a job interview with Elon Musk on Mars.",
        "I can’t make it, the rumors about you turned out to be true.",
        "Raincheck? I’m an exhibit at a science fair that day.",
        "Sorry, a bear chased me and I have no idea where I am.",
        "I can’t make it, turns out shoplifting is illegal!",
        "A painter wants to paint me, least he said he's a painter",
        "Can’t make it, the pot I’m watching hasn’t boiled yet.",
        "Been playing hide n’ seek for a week, no one’s found me yet!",
        "Can’t make it, stuck in the photocopier at work, don’t ask."
    ];

    function randomResponse(accept) {
        if(accept) {
            return acceptResponses[Math.floor(Math.random()*acceptResponses.length)];
        } else {
            return rejectResponses[Math.floor(Math.random()*rejectResponses.length)];
        }
    }

    function isAcceptRsvp() {
        return ($("#rsvp-option").val() == 'Accept')? true : false;
    }

    $("#btn-rsvp-yes").click(function() {
        $("#btn-rsvp-yes").addClass("alt");
        $("#btn-rsvp-no").removeClass("alt");
        $("#rsvp-option").val("Accept");
        $("#modal-rsvp").modal('show');
    });

    $("#btn-rsvp-no").click(function() {
        $("#btn-rsvp-yes").removeClass("alt");
        $("#btn-rsvp-no").addClass("alt");
        $("#rsvp-option").val("Decline");
        $("#modal-rsvp").modal('show');
    });

    $(".open-download-modal").click(function() {
        $("#download-amigo-modal").modal('show');
    });

    $("#modal-rsvp").on('show.bs.modal', function (e) {
        if(isAcceptRsvp()) {
            $("#rsvp-form #rsvp-message").val(inputedMessages.accept || randomResponse(isAcceptRsvp()));
        } else {
            $("#rsvp-form #rsvp-message").val(inputedMessages.decline || randomResponse(isAcceptRsvp()));
        }
    })

    $("#btn-submit-rsvp").click(function(e) {
        e.preventDefault();
        var message = $("#rsvp-form #rsvp-message").val();
        if(isAcceptRsvp()) {
            inputedMessages.accept = message;
        } else {
            inputedMessages.decline = message;
        }
        $.post('/invitation/' + window.location.search, $("#rsvp-form").serialize() + '&response=' + $("#rsvp-option").val(), function(data) {});
        $(".modal").modal('hide');

        if(isAcceptRsvp()) {
            $("#modal-rsvp-success").modal('show');
        } else {
            $("#modal-rsvp-failed").modal('show');
        }
    });

    $('.android-download-btn').click(function(e) {
        $(".modal").modal('hide');
        $("#modal-android-subscription").modal('show');
    });

    if($("#event-date").length>0) {
        $("#event-date").each(function(){
            var clientTimezone = moment.tz.guess();
            var evtDateLink = $(this),
                utcEvtDate = moment.tz(evtDateLink.data("event-date"), 'UTC');

            if (clientTimezone) {
                var clientTime = utcEvtDate.tz(clientTimezone);
                if (utcEvtDate.diff(moment.utc(), 'years') >= 2) {
                    evtDateLink.closest('li').addClass('open-download');
                } else if (moment.utc().subtract(10, 'days') > utcEvtDate || moment.utc().add(10, 'days') < utcEvtDate) {
                    evtDateLink.text(clientTime.format('MMM Do YYYY h:mm a'));
                } else {
                    evtDateLink.text(clientTime.calendar());
                }
            } else {
                evtDateLink.text(utcEvtDate.format('MMM Do YYYY h:mm a'));
            }
        });
    }

    var photoDragging = false;
    $("#user_list").owlCarousel({
        items : 4 ,
        itemsDesktop : false,
        itemsDesktopSmall : false,
        itemsTablet : false,
        itemsMobile : false,
        pagination : false
    });
    
    $("#user_list").mousedown(function(){
        photoDragging = false;
    }).mousemove(function(){
        photoDragging = true
    }).mouseup(function(){
        if(photoDragging === false) {
            $("#download-amigo-modal").modal('show');
        }
    });
});
