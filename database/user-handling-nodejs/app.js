var express = require('express'),
    passport = require('passport'),
    TwitterStrategy = require('passport-twitter').Strategy,
    FacebookStrategy = require('passport-facebook').Strategy,
    GoogleStrategy = require('passport-google').Strategy,
    LinkedInStrategy = require('passport-linkedin').Strategy,
    LocalStrategy = require('passport-local').Strategy,
    ensureLoggedIn = require('connect-ensure-login').ensureLoggedIn,
    app = express(),
    mongoose = require('mongoose'),
    ObjectId = mongoose.Types.ObjectId; 
    extend = require('xtend'),
    crypto = require('crypto'),
    util = require('util'),
    SALT = "s8(hb?.;*!sW";


var UserSchema = new mongoose.Schema({
  providers: [{}],
  name: String,
  image: String,
  email: String,
  password: String,
  dump: String
});

mongoose.connect('mongodb://localhost/scripler');
mongoose.model('User', UserSchema);
var User = mongoose.model('User');

app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.engine('ejs', require('ejs-locals'));
app.use(express.logger());
app.use(express.cookieParser());
app.use(express.bodyParser());
app.use(express.methodOverride());
app.use(express.session({ secret: 'keyboard cat' }));
app.use(passport.initialize());
app.use(passport.session());
app.use(app.router);
app.use(function(err, req, res, next){
  console.error(err.stack);
  res.send(500, 'Something broke: <pre>' + err.stack + '</pre>');
});

passport.serializeUser(function(user, done) {
  done(null, user._id);
});

passport.deserializeUser(function(uid, done) {
  User.findOne({_id: uid}, function (err, user) {
    done(err, user);
  });
});
 

function md5(plain) {
    return crypto.createHash('md5').update(SALT+plain).digest("hex");
} 

 
/*
 * LOCAL ACCOUNT
 */

// Use the LocalStrategy within Passport.
passport.use(new LocalStrategy({usernameField: 'email'}, function(email, password, done) {
    User.findOne({ email: email }, function(err, user) {
        if (err) { return done(err); }
        if (!user) { return done(null, false, { message: 'Unknown user ' + email }); }
        if (user.password == md5(password)) {
            return done(null, user);
        } else {
            return done(null, false, { message: 'Invalid password' });
        }
    });
}));

/*
 * PROVIDER ACCOUNTS
 */
passport.use(new TwitterStrategy({
    consumerKey: "xxxx",
    consumerSecret: "xxxx",
    callbackURL: "http://scripler.com:5000/auth/twitter/callback",
    passReqToCallback: true
  },
  function(req, token, tokenSecret, profile, done) {
    addProviderToUser(profile.provider, profile.id, profile, req.user, done);
  }
));
 
passport.use(new FacebookStrategy({
    clientID: 'xxxx',
    clientSecret: 'xxxx',
    callbackURL: 'http://scripler.com:5000/auth/facebook/callback',
    passReqToCallback: true,
	profileFields: ['id', 'username', 'displayName', 'emails']
  },
  function(req, accessToken, refreshToken, profile, done) {
    addProviderToUser(profile.provider, profile.id, profile, req.user, done);
  }
));
 
passport.use(new GoogleStrategy({
    returnURL: 'http://scripler.com:5000/auth/google/callback',
    realm: 'http://scripler.com:5000/',
    passReqToCallback: true
  },
  function(req, identifier, profile, done) {
    //console.log("DUMP: " + util.inspect(profile, false, null));
    addProviderToUser("google", identifier, profile, req.user, done);
  }
));
 
passport.use(new LinkedInStrategy({
    consumerKey: "xxxx",
    consumerSecret: "xxxx",
    callbackURL: "http://scripler.com:5000/auth/linkedin/callback",
    passReqToCallback: true,
	profileFields: ['id', 'name', 'emails']
  },
  function(req, token, tokenSecret, profile, done) {
    addProviderToUser(profile.provider, profile.id, profile, req.user, done);
  }
));
 
function addProviderToUser(provider, providerId, profile, currentUser, done) {
    var providerObject = {"name": provider, "id": providerId};
    User.findOne({providers: {"$elemMatch": providerObject}}, function(err, user) {
      if(user) {
        //User already in database
        if (currentUser && currentUser._id != user._id) {
            console.log("Current user: " + currentUser);
            console.log("Database user: " + user);
            //TODO merge accounts?
            console.log("debug: " + "User already in database, and already logged in, but not with the same account! Merge!");
            done(null, currentUser);
        } else {
            console.log("debug: " + "Nothing to do... User already has this account attached");
            done(null, user);
        }
      } else {
        if (currentUser) {
            //User already loggedin, so add new provider to user
            var user = currentUser;
            console.log("debug: " + "User already loggedin, so add new provider to user");
            user.providers.addToSet(providerObject);
            done(null, user);
        } else {
            //New user
            //TODO check if another account with same email address exists!
            console.log("debug: " + "New user");
            var user = new User();
            user.providers.addToSet(providerObject);
            user.name = profile.displayName;
            user.email = profile.emails[0].value;
        }
        user.markModified('providers');//"providers" is of type "Mixed", so Mongoose, doesn't detect the change.
        user.save(function(err) {
          if(err) { throw err; }
          done(null, user);
        });
      }
    })
}

app.get('/', function(req, res){
    res.render('index', { user: req.user });
  });
 
app.get('/account',
  ensureLoggedIn('/login'),
  function(req, res) {
    res.render('account', { user: req.user });
  });
 
app.get('/login', function(req, res) {
    res.render('login', { user: req.user, message: req.session.messages });
});
 
//Login with local account 
app.post('/login', function(req, res, next) {
  passport.authenticate('local', function(err, user, info) {
    if (err) { return next(err) }
    if (!user) {
      req.session.messages =  [info.message];
      return res.redirect('/login')
    }
    req.logIn(user, function(err) {
      if (err) { return next(err); }
      return res.redirect('/');
    });
  })(req, res, next);
});

app.get('/new-user', function(req, res) {
    res.render('new-user', { user: req.user, message: req.session.messages });
});
//Create local account
app.post('/new-user', function(req, res, next) {
    //res.send(util.inspect(req.body, false, null));
    var email = req.body.email
    if (!email) {
      req.session.messages =  ["You need to enter an email address!"];
      return res.redirect('/new-user');
    }
    User.findOne({email: email}, function(err, user) {
        if (user) {
          req.session.messages =  ["Email already exists!"];
          return res.redirect('/new-user');
        } else {
            var user = new User();
            user.name = req.body.name;
            user.email = email;
            user.password = md5(req.body.password);
            user.save(function(err) {
              if(err) { return next(err); }
              req.logIn(user, function(err) {
                if (err) { return next(err); }
                return res.redirect('/');
              });
            });
        }
    });
});

app.get('/logout',
  function(req, res) {
    req.logout();
    res.redirect('/');
});

function authnOrAuthz(provider, options) {
    return function (req, res, next) {
        if (!req.isAuthenticated()) {
            passport.authenticate(provider, extend(options, {
                successRedirect: '/settings/accounts', failureRedirect: '/login'
            }))(req, res, next);
        } else {
            passport.authorize(provider)(req, res, next);
        }
    }
}

app.get('/auth/twitter', authnOrAuthz('twitter'));
app.get('/auth/twitter/callback', passport.authenticate('twitter', { successReturnToOrRedirect: '/', failureRedirect: '/login' }));

app.get('/auth/facebook', authnOrAuthz('facebook', { scope: ['email'] }));
app.get('/auth/facebook/callback', passport.authenticate('facebook', { successReturnToOrRedirect: '/', failureRedirect: '/login' }));

app.get('/auth/google', authnOrAuthz('google'));
app.get('/auth/google/callback', passport.authenticate('google', { successReturnToOrRedirect: '/', failureRedirect: '/login' }));

app.get('/auth/linkedin', authnOrAuthz('linkedin', {scope: ['r_basicprofile', 'r_emailaddress']}));
app.get('/auth/linkedin/callback', passport.authenticate('linkedin', { successReturnToOrRedirect: '/', failureRedirect: '/login' }));
  
var server = app.listen(5000);
console.log('Express server started on port %s', server.address().port);