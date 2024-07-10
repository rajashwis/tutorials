/** @odoo-module **/

import { markup, Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./TodoList/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList };

    setup() {
        this.content1 = "<div class='text-primary'>some content</div>";
        this.content2 = markup("<div class='text-primary'>some content</div>");
        this.sum = useState({value: 0});
    }

    incrementSum() {
        this.sum.value++;
    }

}