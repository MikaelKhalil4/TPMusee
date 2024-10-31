import {Component} from './component.js' ; 
import {PRIMS} from '../utils/prims.js' ; 



class Panneau extends Component {

	constructor(data, actor){
		super(data, actor);
		console.log("@@ ",data.name) ; 
        	const panneau = PRIMS.panneau(data.name, data, this.actor.sim.scene);
        	this.actor.object3d = panneau;
	}
}



export {Poster};
