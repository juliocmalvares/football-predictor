import express from 'express';
import routes from './routes';
import cors from 'cors';
import mongoose from 'mongoose';
import path from 'path';
class App{
    constructor(){
        this.server = express();

        mongoose.connect("mongodb+srv://fbpred:fbpred@fbpred-9mob3.mongodb.net/fbpred?retryWrites=true&w=majority", {
            useNewUrlParser: true,
            useUnifiedTopology: true
        }, (err, client) => {
            if(err){
                console.error(err);
                return;
            }
        });   

        this.middlewares();
        this.routes();
    }
    middlewares(){
        this.server.set('view engine', 'ejs');
        this.server.set('views', './src/views');
        this.server.use(cors());
        this.server.use(express.json());
        this.server.use('/files', express.static(path.resolve(__dirname, '..', 'images')));
    }

    routes(){
        this.server.use(routes);
    }
}

export default new App().server;