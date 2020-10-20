import { Router } from 'express';
import NewsController from './controllers/NewsController';

const routes = new Router();



routes.get('/', NewsController.index);
routes.post('/positiva/:id_new', NewsController.update)
routes.post('/negativa/:id_new', NewsController.update)
routes.post('/neutra/:id_new', NewsController.update)
routes.post('/nfutebol/:id_new', NewsController.update)
// routes.put('/', NewsController.update);
export default routes;