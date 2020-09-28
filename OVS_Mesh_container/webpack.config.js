var path = require('path')
var webpack = require('webpack')

module.exports = {
  entry: './src/main.js',
  output: {
    path: path.resolve(__dirname, './dist'),
    publicPath: '/dist/',
    filename: 'build.js'
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          loaders: {
            // Since sass-loader (weirdly) has SCSS as its default parse mode, we map
            // the "scss" and "sass" values for the lang attribute to the right configs here.
            // other preprocessors should work out of the box, no loader config like this necessary.
            'scss': 'vue-style-loader!css-loader!sass-loader',
            'sass': 'vue-style-loader!css-loader!sass-loader?indentedSyntax'
          }
          // other vue-loader options go here
        }
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'file-loader',
        options: {
          name: '[name].[ext]?[hash]'
        }
      }
    ]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    }
  },
devServer: {
    historyApiFallback: true,
    noInfo: true,
    setup(app) {
      var bodyParser = require('body-parser'); 
      app.use(bodyParser.json());
      var fs = require('fs');
      app.post('/url', bodyParser.json(), (req, res) => {
          var stream = fs.createWriteStream("ovs-topo.sh");
          stream.once('open', function () {
              stream.write(req.body["bash-script"]);
              stream.end();
          });

          var stream1 = fs.createWriteStream("windows-node.json");
          stream1.once('open', function () {
              stream1.write(req.body["node"]);
              stream1.end();
          });

          var stream2 = fs.createWriteStream("windows-edge.json");
          stream2.once('open', function () {
              stream2.write(req.body["edge"]);
              stream2.end();
          });

          res.json({ "rafael": 'ok' });
      });
  }
},
  performance: {
    hints: false
  },
  devtool: '#eval-source-map'
}

if (process.env.NODE_ENV === 'production') {
  // change publicPath to './dist/' when env is production
  module.exports.output.publicPath = './dist/'

  module.exports.devtool = '#source-map'
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    })
  ])
}
