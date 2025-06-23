export interface User {
    id: number;
    name: string;
    sex: string,
    imageUrl: string;
}

export class EmptyUser implements User {
    id: number = -1;
    name: string = "default";
    sex: string = "default";
    imageUrl: string = "default";
}