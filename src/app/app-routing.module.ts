import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DataEntryComponent } from './data-entry/data-entry.component';
import { DataListComponent } from './data-list/data-list.component';
import { EditComponent } from './edit/edit.component';
import { PasswordGuard } from './password.guard';
import { EditGuard } from './edit.guard';

const routes: Routes = [
  { path: '', redirectTo: '/data-list', pathMatch: 'full' },
  { path: 'data-entry', component: DataEntryComponent },
  { path: 'data-list', component: DataListComponent,
   canActivate: [PasswordGuard],
 },
  { path: 'edit/:id', component: EditComponent,
   canActivate: [EditGuard],
},
];
@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {

 }
// npx json-server --watch db.json
