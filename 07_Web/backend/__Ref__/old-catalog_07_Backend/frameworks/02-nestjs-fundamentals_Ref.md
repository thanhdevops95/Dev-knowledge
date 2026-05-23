# 🔧 NestJS — Enterprise Node.js Framework

> `[INTERMEDIATE]` — Backend có cấu trúc, scalable, maintainable

---

## NestJS là gì?

Framework Node.js lấy cảm hứng từ Angular — dùng **TypeScript + Decorators + Dependency Injection** để xây dựng server-side applications có kiến trúc rõ ràng.

```
Express:   Tự do, ít quy tắc → dễ messy khi scale
NestJS:    Cấu trúc chuẩn, DI, Modules → enterprise-grade
```

---

## 1. Kiến trúc Module → Controller → Service

```
┌──────────────┐
│    Module     │  ← Gom liên quan lại (Users, Auth, Orders...)
├──────────────┤
│  Controller   │  ← Xử lý HTTP (routes, request/response)
├──────────────┤
│   Service     │  ← Business logic (query DB, tính toán)
├──────────────┤
│   Repository  │  ← Data access (Prisma, TypeORM)
└──────────────┘
```

```typescript
// users.module.ts
import { Module } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
    imports: [PrismaModule],
    controllers: [UsersController],
    providers: [UsersService],
    exports: [UsersService],  // Cho modules khác dùng
})
export class UsersModule {}
```

---

## 2. Controller — Xử lý HTTP

```typescript
import { Controller, Get, Post, Put, Delete, Param, Body, Query, UseGuards, HttpCode } from '@nestjs/common';
import { UsersService } from './users.service';
import { CreateUserDto, UpdateUserDto } from './dto';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('api/users')
export class UsersController {
    constructor(private readonly usersService: UsersService) {}

    @Get()
    findAll(
        @Query('page') page = 1,
        @Query('limit') limit = 20,
    ) {
        return this.usersService.findAll({ page: +page, limit: +limit });
    }

    @Get(':id')
    findOne(@Param('id') id: string) {
        return this.usersService.findOne(id);
    }

    @Post()
    @HttpCode(201)
    create(@Body() createUserDto: CreateUserDto) {
        return this.usersService.create(createUserDto);
    }

    @Put(':id')
    @UseGuards(JwtAuthGuard)  // Bảo vệ route
    update(@Param('id') id: string, @Body() updateUserDto: UpdateUserDto) {
        return this.usersService.update(id, updateUserDto);
    }

    @Delete(':id')
    @UseGuards(JwtAuthGuard)
    remove(@Param('id') id: string) {
        return this.usersService.remove(id);
    }
}
```

---

## 3. Service — Business Logic

```typescript
import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateUserDto, UpdateUserDto } from './dto';

@Injectable()
export class UsersService {
    constructor(private prisma: PrismaService) {}

    async findAll({ page, limit }: { page: number; limit: number }) {
        const [data, total] = await Promise.all([
            this.prisma.user.findMany({
                skip: (page - 1) * limit,
                take: limit,
                select: { id: true, name: true, email: true, role: true },
            }),
            this.prisma.user.count(),
        ]);

        return {
            data,
            meta: {
                page,
                limit,
                total,
                totalPages: Math.ceil(total / limit),
            },
        };
    }

    async findOne(id: string) {
        const user = await this.prisma.user.findUnique({
            where: { id },
            include: { posts: { take: 5 } },
        });
        if (!user) throw new NotFoundException(`User ${id} not found`);
        return user;
    }

    async create(dto: CreateUserDto) {
        const hashedPassword = await bcrypt.hash(dto.password, 12);
        return this.prisma.user.create({
            data: { ...dto, password: hashedPassword },
        });
    }

    async update(id: string, dto: UpdateUserDto) {
        await this.findOne(id);  // Throws if not found
        return this.prisma.user.update({ where: { id }, data: dto });
    }

    async remove(id: string) {
        await this.findOne(id);
        return this.prisma.user.delete({ where: { id } });
    }
}
```

---

## 4. DTOs & Validation

```typescript
import { IsString, IsEmail, MinLength, IsOptional, IsEnum } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class CreateUserDto {
    @ApiProperty({ example: 'Nguyễn An' })
    @IsString()
    @MinLength(2)
    name: string;

    @ApiProperty({ example: 'an@mail.com' })
    @IsEmail()
    email: string;

    @IsString()
    @MinLength(8)
    password: string;

    @IsOptional()
    @IsEnum(['user', 'admin'])
    role?: 'user' | 'admin';
}

// Validation pipe (main.ts)
app.useGlobalPipes(new ValidationPipe({
    whitelist: true,      // Strip unknown properties
    forbidNonWhitelisted: true,
    transform: true,      // Auto-transform types
}));
```

---

## 5. Guards, Interceptors, Pipes

```
Request lifecycle:
  Middleware → Guard → Interceptor (before) → Pipe → Handler → Interceptor (after) → Filter

Guard:       Xác thực / phân quyền
Pipe:        Transform / validate input
Interceptor: Logging, caching, transform response
Filter:      Xử lý exceptions
```

```typescript
// JWT Guard
@Injectable()
export class JwtAuthGuard implements CanActivate {
    constructor(private jwtService: JwtService) {}

    canActivate(context: ExecutionContext): boolean {
        const request = context.switchToHttp().getRequest();
        const token = request.headers.authorization?.split(' ')[1];
        if (!token) throw new UnauthorizedException();

        try {
            request.user = this.jwtService.verify(token);
            return true;
        } catch {
            throw new UnauthorizedException('Invalid token');
        }
    }
}

// Logging Interceptor
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
    intercept(context: ExecutionContext, next: CallHandler) {
        const request = context.switchToHttp().getRequest();
        const now = Date.now();

        return next.handle().pipe(
            tap(() => {
                console.log(`${request.method} ${request.url} — ${Date.now() - now}ms`);
            }),
        );
    }
}

// Global exception filter
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
    catch(exception: unknown, host: ArgumentsHost) {
        const ctx = host.switchToHttp();
        const response = ctx.getResponse();

        const status = exception instanceof HttpException
            ? exception.getStatus()
            : 500;

        response.status(status).json({
            statusCode: status,
            message: exception instanceof Error ? exception.message : 'Internal error',
            timestamp: new Date().toISOString(),
        });
    }
}
```

---

## 6. Swagger Auto-docs

```typescript
// main.ts
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';

const config = new DocumentBuilder()
    .setTitle('My API')
    .setVersion('1.0')
    .addBearerAuth()
    .build();

const document = SwaggerModule.createDocument(app, config);
SwaggerModule.setup('api/docs', app, document);
// → Interactive docs at http://localhost:3000/api/docs
```

---

## Bài tập thực hành

- [ ] NestJS project: CRUD Users + Posts với Prisma
- [ ] Auth module: JWT login, register, guards
- [ ] Swagger documentation tự động
- [ ] Interceptor: response time logging + caching

---

## Tài nguyên thêm

- [NestJS Docs](https://docs.nestjs.com/) — Official
- [NestJS Prisma Recipe](https://docs.nestjs.com/recipes/prisma) — Database
