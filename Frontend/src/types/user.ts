export interface User {
	id: number;
	name: string;
	sex: string;
	imageUrl: string;
}

export default class EmptyUser implements User {
	id = 0;
	name = '';
	sex = '';
	imageUrl = '';
}
